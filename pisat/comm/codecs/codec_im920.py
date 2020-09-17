#! python3
#
#
#
#
#
#

class CodecIm920:

    """
    codec for sending sensors' data

    Attributes
    ----------
    tags : list
        tugs of data
    packet : int
        data capacity that can be send once
    """

    REQUEST_FLAG = "00"

    def __init__(self, tags:tuple, packet:int=64):
        """
        Parameter
        ---------
        tags : tuple, list 
            tugs of data
        packet : int, default 64
            data capacity that can be send once
        """
        self.tags = list(tags)      # list
        self.packet = packet        # int

    def encoder(self, flag:str, tag_data:dict)-> "encoded data:str":
        """
        encode given data 

        Parameter
        ---------
        flag : str
            flag code
        tag_data : dict
            the keys are tags of data and the values are their data

        Returns
        -------
        data_encoded : str
            encoded data
        """

        data_encoded = []               # initilize as a list
        data_encoded.append(flag)       # append flag data first

        # append each tag and data transformed into str
        for key, val in tag_data.items():

            val = str(val)

            # if a packet is full, then rest of data is ignored and not sent
            tag_packet = len(key) + len(val)
            if self.packet - tag_packet < len(data_encoded):
                print("caution: can't encode all data because of too much packet, but send some of it.")
                break

            data_encoded.append(key)
            data_encoded.append(val)

        return "".join(data_encoded)        # transform a list into a str

    # search tags 
    def __find_tag(self, data:list):
        tag_notset = [i for i in data if "A" <= i <= "z"]

        for tag in tag_notset:
            self.tags.append(tag)

    # extracts data corresponded to a tag
    def __extract_data(self, data:list)-> "tag:str, data_tag:list, data_rest:list":

        data = data
        tag = data.pop(0)       # the head of data should be a tag
        data_tag = []           # initialize data corresponded to the tag as a list

        if tag in self.tags:

            # append data to data_tag until the next tag is found 
            while not(data[0] in self.tags):

                # case in which you have not set (a/) tag(/s)
                if "A" <= data[0] <= "z":
                    self.__find_tag(data)
                    break

                data_tag.append(data.pop(0))

                # all data was read
                if data == []:
                    break

            return tag, data_tag, data      # "data" means rest of data 

        else:
            print("error")
            return None, None, None

    # reshape list of str data into floats
    @staticmethod
    def reshape_data(data:list)-> "reshaped data:float":
        data_reshaped = "".join(data)
        return float(data_reshaped)

    def decoder(self, data:str)-> "flag:str, data_decoded:dict":
        """
        decode a series of raw data

        Parameter
        ---------
        data : str 
            raw data recieved

        Returns
        -------
        flag : str
            extracted flag of given data
        data_decoded : dict
            decoded data
        """
        
        flag = "".join([data.pop(0), data.pop(0)])

        # process a request 
        if flag == REQUEST_FLAG:
            return flag, int(data)

        data = list(data)
        data_decoded = {}

        while data != []:
            tag, data_list, data = self.__extract_data(data)    
            data_decoded[tag] = CodecIm920.reshape_data(data_list)           # append a tag and data

        return flag, data_decoded

    def formater(self, data_decoded:dict)-> "data_formatted":
        """
        this method puts data into a format. 

        Parameter
        ---------
        data_decoded : dict 
            data already decoded with decoder method
        
        Returns
        -------
        data_formatted : dict
            
        """
        tag_notget = [tag for tag in self.tags if not(tag in data_decoded.keys())]
        for tag in tag_notget:
            data_decoded[tag] = None

        return data_decoded


if __name__ == "__main__":
    tags = ("P", "T", "H")
    coder = CodecIm920(tags)
    data = {"P": 1.012, "T": 20.3}
    encoded_data = coder.encoder("21", data)
    print("encoded data:", encoded_data)

    flag, decoded_data = coder.decoder(encoded_data)

    print("flag:", flag)
    print("decoded data:", decoded_data)

    formatted_data = coder.formater(decoded_data)
    print("formatted_data:", formatted_data)
