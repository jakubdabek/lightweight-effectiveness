# Discovering class-test pairs
This process primitively looks for the `surefire` plugin in `pom.xml` with its `include` and `exclude` patterns,
and globs the project files.  
This misses nuance when dealing with `AllTests` style tests, when all test classes are listed on an attribute in java code.  
TODO: other discovery algorithm for `AllTests` pattern.  
TODO: Gradle

Classes corresponding to test classes are searched by removing the `Test` part of the test class
depending on the include pattern (e.g. `FooTest -> Foo` or `BarTestCase -> Bar`),
but without taking into account the full path, e.g. having `org.foo.BarTest` test, `org.foo.Bar` *and* `org.baz.Bar` classes,
the current algorithm will find both of the classes, even though the second one is (probably) unrelated (see `*.Payload` in `cat/cat-home`).
TODO: take full paths into account while searching.


# Buidling specific projects

## OpenGrok
Requires `git`, `subversion`, `ctags` for build, other version control tools are optional (?) for tests (`mercurial`, `cssc`, `cvs`, `brz`).  
Requires **non-root** user for tests (see `PageConfigTest`).

## Junit4
Testing with PIT only works after building the project once and not using `mvn clean`, because of a conflict of Junit versions on classpath.
