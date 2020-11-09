
from typing import Dict, Tuple, Union

from pisat.comm.transceiver.socket_transceiver import SocketTransceiver
from pisat.comm.transceiver.request import (
    CommandBase, ResponseBase, RequestCommandError,
    InvalidRequestError, Request
)


class CommandServer:
    
    COMMAND_RESPONSE = ResponseBase.COMMAND
    
    def __init__(self, transceiver: SocketTransceiver, request: Request) -> None:
        self._transceiver = transceiver
        self.request = request
        self._CtoF: Dict[bytes, CommandBase] = {}             # Command to Function
    
    def append(self, *commands: Tuple[CommandBase, ...]) -> None:
        for command in commands:
            if not issubclass(command, CommandBase):
                raise TypeError(
                    "'commands' must include only CommandBase."
                )
                
            self._CtoF[command.COMMAND] = command
    
    def start_serve(self, timeout: Union[float, int] = -1.) -> None:
        if not len(self._CtoF):
            raise RequestCommandError(
                "No command has been registerd yet."
            )
        
        if not isinstance(timeout, (float, int)):
            raise TypeError(
                "'timeout' must be float or int."
            )
        
        try:
            while True:
                sock = self._transceiver.listen(timeout)
                if sock is None:
                    break
                
                params = self.request.parse_request(sock)
                
                # ignore other server's response
                if params.command == self.COMMAND_RESPONSE:
                    continue
                
                command = self._CtoF.get(params.command)
                if command is None:
                    raise InvalidRequestError(
                        "Invalid command has been detected. " + 
                        f"COMMAND: {params.command}"
                    )
                
                command.exec(sock, params)
                
        except KeyboardInterrupt:
            pass
