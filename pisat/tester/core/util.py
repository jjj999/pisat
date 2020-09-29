
from typing import Any, Callable, Optional, Sequence, Tuple
import csv


def simulate_judge_from(judge: Callable,
                        my_flag: Any, 
                        path: str, 
                        dnames: Optional[Sequence[str]] = None) -> int:
    """Simulate given judge function and find the index on which a flag is detected.
    
    This function executes given judge function with data of given file 
    and returns the result as the index on which a flag except for 'my_flag' 
    is triggered. If any flags are not triggered, then the method
    returns -1. Make sure that 'my_flag' is not None.

    Parameters
    ----------
        judge : Callable
            Function with same interface as Node.judge
        my_flag : Any
            flag for moving itself, not None
        path : str
            Path of a csv file.
        dname : Optional[Sequence[str]], optional
            Data names if the csv file doesn't have them, by default None

    Returns
    -------
        int
            The index on which a flag except for 'my_flag' is triggered.

    Raises
    ------
        ValueError
            path must reprents path of a csv file.
    """
    if not path.endswith(".csv"):
        raise ValueError(
            "'path' must be a csv file."
        )
        
    if my_flag is None:
        raise ValueError(
            "'my_flag' must not be None because None represents an end Node."
        )
        
    with open(csv, "rt") as f:
        reader = csv.DictReader(f, dnames)
        
        for i, data in enumerate(reader):
            judged = judge(data)
            if judged != my_flag:
                return i
            
        return -1

def simulate_judge_from_all(judge: Callable, 
                            path: str, 
                            dnames: Optional[Sequence[str]] = None) -> Tuple[Any]:
    """Simulate given judge function by feeding data from given file.
    
    This funcition executes given judge function with data in given file 
    and collects the results of the judge function.

    Parameters
    ----------
        judge : Callable
            Function with same interface as Node.judge
        path : str
            Path of a csv file.
        dname : Optional[Sequence[str]], optional
            Data names if the csv file doesn't have them, by default None

    Returns
    -------
        Tuple[Any]
            Returned results from the given judge function.

    Raises
    ------
        ValueError
            path must reprents path of a csv file.
    """
    if not path.endswith(".csv"):
        raise ValueError(
            "'path' must be a csv file."
        )
        
    with open(csv, "rt") as f:
        reader = csv.DictReader(f, dnames)
        result = []
        
        for data in reader:
            result.append(judge(data))
            
    return tuple(result)
    