import time

final_num = 10
window_size = 3

for x in range(final_num - window_size + 2):
    _x_ = []
    for y in range(x, x+window_size):
        _x_.append(y)
    print(_x_)


class timer(object):
    def __init__(self, seconds):
        self.seconds = seconds
        self.timeout = False
        self.start_time = None
        self.end_time = None
    
    def start_timer(self): # Start timer
        self.start_time = time.time()

    def end_timer(self): # End timer
        self.end_time = time.time()

    def is_timeout(self): # Checks if the timer is greater than timeout
        try:
            self.end_timer()
            if (self.end_time - self.start_time > self.seconds):
                print('TIMEOUT!')
                return True
                
            else:
                print('No timeout. You have: ' + str(self.seconds - (self.end_time - self.start_time)) + ' seconds left!')
                return False
                
        except Exception:
            raise Exception('Must start timer!')

if __name__ == '__main__':
    continue
    # timer = timer(0.1)
    # timer.start_timer()
    # time.sleep(0.097)
    # print(timer.is_timeout())