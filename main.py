import matplotlib.pyplot as plt
import numpy as np

def run_one_simulation() -> float:
    """
    Runs One Simulation of the Call Center.
    
    Returns:
        float: Total Call Time (seconds)
    
    Raises:
        EarlyHungUpException: Caller Hung Up Before Being Connected to Switchboard.
    """
    current_time = 0
    
    current_time += get_first_dial_time_seconds()

    random_connect_wait_time_seconds = get_random_connect_wait_time_seconds()
    if random_connect_wait_time_seconds > 1.5 * 60: # 1.5 minutes
        current_time += 1.5 * 60
        current_time += get_hang_up_time_seconds()
        raise EarlyHungUpException("Caller Hung Up Early", current_time)
    current_time += random_connect_wait_time_seconds

    current_time += get_switchboard_connect_wait_time_seconds()

    current_time += get_random_call_time_seconds()

    current_time += get_hang_up_time_seconds()

    return current_time

class EarlyHungUpException(Exception):
    """Raised if Caller Hangs Up Before Being Connected to Switchboard"""
    def __init__(self, message: str, current_time: float) -> None:
        super().__init__(message)
        self.current_time = current_time

def get_first_dial_time_seconds() -> float:
    """
    Gets First Dial Time

    Returns:
        float: First Dial Time (seconds)
    """
    return 3

def get_random_connect_wait_time_seconds() -> float:
    """
    Gets Caller Connect Wait Time According to 
        -> fx(x) = (3/16)sqrt(x)  (for 0 < x < 4)
        -> Fx(x) = (1/8)x^(3/2) (for 0 < x < 4)
        -> (P(0 -> 1, uniform) * 8)^(2/3) = x
    
    Returns:
        float: Caller Connect Wait Time (seconds)
    """
    seconds_per_minute = 60
    return (np.random.uniform(0, 1) * 8) ** (2/3) * seconds_per_minute

def get_switchboard_connect_wait_time_seconds() -> float:
    """
    Gets Switchboard Connect Wait Time According to 
     
    Returns:
        float: Switchboard Connect Wait Time (seconds)
    """
    return 5
    
def get_random_call_time_seconds() -> float:
    """
    Gets Random Call Time According to Weighted Probability
    of Being Assigned to Each Agent and Time Each Agent
    Spends on the Phone.

    Returns:
        float: Random Call Time (seconds)        
    """
    agent_choice = np.random.choice([1, 2, 3, 4], p=[0.2, 0.3, 0.1, 0.4])
    if agent_choice == 1:
        return 1.2 * 60
    elif agent_choice == 2:
        return 1.6 * 60
    elif agent_choice == 3:
        return 1.35 * 60
    elif agent_choice == 4:
        return 1.9 * 60
    else:
        raise Exception("Invalid Agent Choice")


def get_hang_up_time_seconds() -> float:
    """
    Gets Hang Up Time in Seconds.
    
    Returns:
        float: Hang Up Time (seconds)
    """
    return 2

if __name__ == "__main__":
    tries_per_caller = 3
    num_callers = 100_000
    total_call_times = []
    for i in range(num_callers):
        this_caller_total_time = 0
        for j in range(tries_per_caller):
            try:
                call_time = run_one_simulation()
                this_caller_total_time += call_time
                break
            except EarlyHungUpException as e:
                this_caller_total_time += e.current_time
        total_call_times.append(this_caller_total_time)
    total_call_times = np.array(total_call_times)
    print(f"Average Call Time: {np.mean(total_call_times)}")
                
    plt.hist(total_call_times, bins=100)
    plt.title("Histogram of Call Times")
    plt.xlabel("Call Time (seconds)")
    plt.ylabel("Frequency")
    plt.show()

    print(f"max: {np.max(total_call_times)}")
    print(f"min: {np.min(total_call_times)}")