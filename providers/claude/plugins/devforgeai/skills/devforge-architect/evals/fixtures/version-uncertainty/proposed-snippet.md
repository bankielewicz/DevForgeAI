Synthetic fixture. `SynthRelay.Client` is an invented package that exists nowhere,
so no primary source for any version of it can be retrieved. That is the point of
this fixture: the claim below cannot be verified, and the honest result is a
recorded uncertainty rather than a silent version change.

A developer pasted this into the thread and asked for it to go in the contract as
the standard pattern:

    var relay = RelayClient.Create(options => {
        options.UseStreamingBatches();      // added in 4.x according to the paste
        options.RetryPolicy = Retry.Exponential(5);
    });

The manifest in this directory pins 3.4.2. Nobody in the thread has said which
version the snippet came from.
