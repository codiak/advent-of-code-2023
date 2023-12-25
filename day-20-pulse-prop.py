import math
import re

from utils import loadInputFile

text_data = loadInputFile("day-20.txt")

example = """
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""
example_2 = """
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
output ->
"""

# text_data = example_2

lines = text_data.strip().split('\n')
module_map = {}
pulse_queue = []
low_sent = 0
high_sent = 0
conjunctions = []


class Module:
    def __init__(self, name: str, flipflop: bool, state: int, conjunction: bool):
        self.name = name
        self.flipflop = flipflop
        self.conjunction = conjunction
        self.state = state
        self.memory = {}
        self.destinations = []

    def sig_to_ds(self, level):
        queue = []
        for d in self.destinations:
            queue.append((self.name, d, level))
        return queue

    def conjunction_state(self):
        if sum(self.memory.values()) == len(self.memory):
            return 0
        else:
            return 1

    def pulse(self, source, level):
        send_level = 1
        if self.flipflop and level == 1:
            return []
        elif self.flipflop and level == 0:
            self.state = 1 - self.state
            send_level = self.state
        elif self.conjunction:
            self.memory[source] = level
            send_level = self.conjunction_state()
        else:
            # broadcaster
            send_level = level
        return self.sig_to_ds(send_level)

# Build modules
for line in lines:
    parts = line.split('->')
    source = parts[0].strip()
    dest = parts[1].strip().split(',')
    flipflop = False
    conjunction = False
    if source.startswith('%'):
        flipflop = True
        source = source[1:]
    elif source.startswith('&'):
        conjunction = True
        source = source[1:]
        conjunctions.append(source)
    module = Module(source, flipflop, 0, conjunction)
    for d in dest:
        d_name = d.strip()
        module.destinations.append(d_name)
    module_map[source] = module

# Set conjunction input defaults
for m in module_map.values():
    print(m.name, m.destinations)
    for d in m.destinations:
        if d in conjunctions:
            module_map[d].memory[m.name] = 0

conj_send_lo = {}
button_presses = 10000
rx_first_pulse = None

for press in range(button_presses):
    print(f"🔘 Button press {press+1}")
    # button -> broadcaster
    low_sent += 1

    for d in module_map['broadcaster'].destinations:
        pulse_queue.append(('broadcaster', d, 0))

    while len(pulse_queue) > 0:
        # print(f"pulse_queue: {pulse_queue}")
        source, target, level = pulse_queue.pop(0)
        if target:
            if target == 'rx' and level == 0:
                if rx_first_pulse is None:
                    rx_first_pulse = button_presses
            if source in conjunctions and level == 0:
                if source not in conj_send_lo:
                    conj_send_lo[source] = press+1
            # print(f"pulse: {source} -> {target} ({level})")
            if level == 0:
                low_sent += 1
            else:
                high_sent += 1
            if target in module_map:
                receiver = module_map[target]
                pulse_queue.extend(receiver.pulse(source, level))


print(f"🎁 Part 1, low: {low_sent}, high: {high_sent}, product: {low_sent * high_sent}")

conjunction_alignment = math.lcm(*conj_send_lo.values())

print(f"🎁 Part 2, low pulse to rx: {conjunction_alignment} presses"
)
