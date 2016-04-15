Compatibility test generator files

These files are works as `md` documentation.
Since `md` is treated specially, one has to copy&paste one of these
files to `codec-template-md.ftl` and run

mvn clean compile -Dhazelcast.generator.md=TRUE .
