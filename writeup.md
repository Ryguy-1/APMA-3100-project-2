# Analyzing Customer Wait Times for A Ticketing Service

### The given scenario is about waiting times for customers calling a ticketing agency. This paper will analyze various statistics about W, a random variable which represents the wait times. W is based on a person's journey through the ticketing process. It takes into account dialing times, hang up times, waiting to be connected with a switchboard, and waiting to be connected with an agent. Customers can also decide to hang up and call again later for a maximum of 3 total calls.

### We have developed computer code to help answer some questions that the ticketing agency may have about their customer's wait times. Let's look at the two extremes first. The least amount of time possible for a customer to wait during the process is 82 seconds, and the most is 304 seconds. Therefore, the range of possible values for W is 82 <= W <= 404. These two values were calculated in the following manner:

## MIN:

### 3 seconds to call + 0 seconds waiting for the switchboard + 5 seconds waiting to connect to an agent + 72 seconds to get the ticket with the fastest agent + 2 seconds to hang up = 82 seconds total.

## MAX:

### The max scenario will occur will the customer fails to get a ticket the first two times, then gets a ticket on the third try. This is represented like so:

### 2(3 seconds to call + 90 seconds waiting for the switchboard + 2 seconds hanging up) + (3 seconds to call + 90 seconds waiting for the switchboard + 5 seconds waiting to connect to an agent + 114 seconds to get the ticket with the slowest agent + 2 seconds to hang up) = 404 seconds total

### Another question the ticketing agency may have is about the average and median wait times for a customer. Using our computer algorithm, we have found that the expected wait time it EXPECTEDWAITTIMEEEE. In other words, E[W] = EXPECTEDWAITTIMEEE. The median wait time is MEDIANWAITTIMEEE. Here is a visual representation of the cumulative distribution of wait times to help put these values into context:

# GRAPHICALDISTRIBUTIONOFW

# FW(W) - CDF of W

### Lastly, we can also look at the [general way to say PDF] for the wait times:

# PDF HISTOGRAM

### You may notice one or more spikes in your histogram. Give the value(s) of the spike(s), and give an explanation for what is going on with them.

---

### On our honor, we have not gotten any outside help on this project, except from the instructor or TA or your partner. Signed:

### Marcus Muntean, Ryland Birchmeir
