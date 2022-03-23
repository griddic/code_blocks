from enum import Enum, auto

from transitions import Machine
from transitions.extensions import GraphMachine


class State(Enum):
    LAY = auto()
    STAY = auto()
    RUN = auto()

    @property
    def value(self):
        return self.name


def new_machine(base_cls=None):
    if base_cls == None:
        m = Machine(states=State, initial=State.LAY)
    else:
        m = base_cls(states=State, initial=State.LAY)
    m.add_transition('stand_up', State.LAY, State.STAY)

    m.add_transition('run', State.STAY, State.RUN)
    m.add_transition('lay', State.STAY, State.LAY)

    m.add_transition('lay', State.RUN, State.LAY)
    return m


# class SM:
#     def __init__(self):
#         self._machine = new_machine()
#

if __name__ == '__main__':
    m = new_machine(base_cls=GraphMachine)
    print(m.state)
    m.stand_up()
    print(m.state)
    m.lay()
    print(m.state)

    m.get_graph().draw('my_state_diagram.png', prog='dot')
