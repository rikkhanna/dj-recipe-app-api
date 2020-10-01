Some Concepts:-

Advanced area of testing mocking

Mocking: is when you override or change the behavior of the dependencies of the code you are testing.

we use mocking to avoid unintended side-effects

When Writing Unit Tests:

- Never depend on external services.
  - This because you can not guarantee that the service will be available at the point that you run the test.
  - This would make the test unpredictable/unreliable
- Sending spam emails
- Clogging up email server

* Management Command: This command will allow us to wait for the database to be available before continuing and running other commands.
