# Sample testbench for a Tiny Tapeout project

There is a default testbench in `test/test.py`. See [https://docs.spade-lang.org/simulation.html](https://docs.spade-lang.org/simulation.html) for more information on testing Spade designs.

The tests are run both pre- and post-synthesis, however if you decide to write unit tests for sub-components they will not work in the post-synthesis tests as only the top unit is synthesized.
