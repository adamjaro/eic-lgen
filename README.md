# Event generator for luminosity studies at the EIC

## Run

<pre><code> ./lgen.py lgen_18x275.ini </pre></code>

- lgen_18x275.ini is an example configuration for the EIC top energy. The configuration is in INI format.
- It might be necessary to adjust Python interpreter in lgen.py

## Outputs

- .dat: pythia6 text format
- .tx: TX format
- .root: TTree with selected variables

## Dependencies

- Python 2.7

## References

- Eur.Phys.J. C71 (2011) 1574
- H1-04/93-287

