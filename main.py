import matplotlib.pyplot as plt
import numpy as np


def main() -> None:
    tries_per_caller = 3
    num_callers = 1_000_000
    total_call_times = []
    for i in range(num_callers):
        this_caller_total_time = 0
        for _ in range(tries_per_caller):
            try:
                call_time = run_one_simulation()
                this_caller_total_time += call_time
                break
            except EarlyHungUpException as e:
                this_caller_total_time += e.current_time
        total_call_times.append(this_caller_total_time)
    total_call_times = np.array(total_call_times)

    expected_call_time = np.mean(total_call_times)
    min_call_time = np.min(total_call_times)
    max_call_time = np.max(total_call_times)
    median_call_time = np.median(total_call_times)
    list_of_people_who_failed = total_call_times[total_call_times == 285]
    percent_failed_tickets = len(list_of_people_who_failed) / len(total_call_times)
    percent_got_tickets = 1 - percent_failed_tickets

    # CDF Estimation
    total_call_times.sort()
    num_cdf_bins = 50
    cdf_range_space = round(
        max_call_time - min_call_time
    )  # equals range at certain num sims high enough
    cdf_bin_size = cdf_range_space / num_cdf_bins
    cdf_bins = np.arange(round(min_call_time), round(max_call_time), cdf_bin_size)
    cdf_bin_counts = np.zeros(num_cdf_bins)
    for i in range(num_cdf_bins):
        cdf_bin_counts[i] = len(total_call_times[total_call_times < cdf_bins[i]])

    # ---- Printouts ----
    print(
        f"Range of Values: {min_call_time} to {max_call_time} = {max_call_time - min_call_time}"
    )
    print(f"Expected Call Time: {expected_call_time}")
    print(f"Median Call Time: {median_call_time}")
    print(f"Distribution Shown Now.")
    plt.hist(total_call_times, bins=25)
    plt.title(
        "Histogram of Call Times (# of Calls/1_000_000 vs Call Time (seconds)) (20 Bins)"
    )
    plt.xlabel("Call Time (seconds)")
    plt.ylabel("# of Calls/1_000_000")
    plt.show()
    print(f"Probability Caller Gets Tickets: {percent_got_tickets}")
    print(f"CDF Shown Now.")
    plt.plot(cdf_bins, cdf_bin_counts / len(total_call_times))
    plt.title("CDF of Call Times (Percent of Calls <= Call Time vs Call Time (seconds))")
    plt.xlabel("Call Time (seconds)")
    plt.ylabel("Percent of Calls <= Call Time")
    plt.show()
    print(f"--- CDF Table ---")
    max_bin_width = max(len(f"{bin_value:.3f}") for bin_value in cdf_bins)
    max_count_width = max(
        len(f"{count/len(total_call_times):.3f}") for count in cdf_bin_counts
    )
    for i in range(len(cdf_bin_counts)):
        print(
            f"| x = {cdf_bins[i]:{max_bin_width}.3f} , Fx(x) = {cdf_bin_counts[i]/len(total_call_times):{max_count_width}.3f} |"
        )
    print(f"| x = {round(max_call_time):.3f} , Fx(x) = 1.000 |")


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
    if random_connect_wait_time_seconds > 1.5 * 60:  # 1.5 minutes
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
    return (np.random.uniform(0, 1) * 8) ** (2 / 3) * seconds_per_minute


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
    main()
