.PHONY: install dev build preview new run today check watch submit test

install:
	cd frontend && npm install

dev:
	cd frontend && npm run dev

build:
	cd frontend && npm run build

preview: build
	cd frontend && npm run preview

## Run a solution locally (auto-reads from inputs/YEAR/dayDD.txt if it exists)
## Usage: make run YEAR=2024 DAY=01
##        make run YEAR=2024 DAY=01 INPUT=path/to/input.txt
##        make run YEAR=2024 DAY=01 VIZ=1
run:
	@test -n "$(YEAR)" || (echo "Usage: make run YEAR=2024 DAY=01 [INPUT=...] [VIZ=1]" && exit 1)
	@test -n "$(DAY)"  || (echo "Usage: make run YEAR=2024 DAY=01 [INPUT=...] [VIZ=1]" && exit 1)
	@python3 run.py $(YEAR) $(DAY) \
		$(if $(INPUT),--input $(INPUT),) \
		$(if $(VIZ),--viz,)

## Scaffold a new solution
## Usage: make new YEAR=2024 DAY=02
new:
	@test -n "$(YEAR)" || (echo "Usage: make new YEAR=2024 DAY=02" && exit 1)
	@test -n "$(DAY)"  || (echo "Usage: make new YEAR=2024 DAY=02" && exit 1)
	@mkdir -p solutions/$(YEAR)/day$(DAY)
	@cp -n solutions/template/solution.py solutions/$(YEAR)/day$(DAY)/solution.py 2>/dev/null || true
	@cp -n solutions/template/meta.json   solutions/$(YEAR)/day$(DAY)/meta.json   2>/dev/null || true
	@echo "Created solutions/$(YEAR)/day$(DAY)/"

## Daily workflow (YEAR/DAY default to today's puzzle, see aoc.py)
## Usage: make today                 scaffold solution, download input, create example files
##        make check                 run solve() on the examples, then on the real input
##        make watch                 re-run check every time a file of the day is saved
##        make submit PART=1         run on the real input and submit after a y/N prompt
##        make submit PART=2 FORCE=1 submit even when an example fails
##        make today YEAR=2025 DAY=03
today check watch:
	@python3 aoc.py $@ $(YEAR) $(DAY)

submit:
	@test -n "$(PART)" || (echo "Usage: make submit PART=1 [YEAR=2026 DAY=01] [FORCE=1]" && exit 1)
	@python3 aoc.py submit $(YEAR) $(DAY) --part $(PART) $(if $(FORCE),--force,)

## Run the tests of the workflow tooling
test:
	@python3 -m unittest discover -s tests
