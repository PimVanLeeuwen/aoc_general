.PHONY: install dev build preview new run

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
