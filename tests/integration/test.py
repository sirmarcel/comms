from comms import Comms

comms = Comms(prefix="testing")

from time import sleep

comms.announce("testing...")

reporter = comms.reporter()
reporter.start("doing a job")
reporter.step("with a task")
sleep(0.5)
comms.talk("a message emitted during the task")
sleep(0.2)
reporter.step("another task")
sleep(1.5)
reporter.step("yet another task")
sleep(2.5)
comms.warn("unexpected message!!")
sleep(1)
reporter.step("many short steps", spin=False)
for i in range(10000):
    reporter.tick(f"i={i}")
    sleep(0.0001)

sleep(0.2)
reporter.step("some final task")
sleep(0.2)
comms.talk("a message emitted during the task")
sleep(1.8)
reporter.step("some final very short task")
comms.talk("a message emitted during the task")

reporter.done()
