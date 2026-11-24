FF    ?= FreeFem++-nw
FFOPT ?= -v 0
PY    ?= python3
K     ?= 2
NU    ?= 0.1

SHELL := /bin/bash
.SHELLFLAGS := -o pipefail -c
RUN = $(FF) $(FFOPT)

.PHONY: help all q1 q2 q2-k2 q2-k3 q3 q4 figures clean

help:
	@echo "make q1      [K=2|3] [N=16]           validation (Newton + erreurs)"
	@echo "make q2      [NMIN=4] [NMAX=128]      convergence P2-P1-P2 et P3-P2-P3"
	@echo "make q2-k2 / make q2-k3               un seul ordre"
	@echo "make q3      [NMIN=8] [NMAX=64]       effet de la viscosite (k=2)"
	@echo "make q4      [NU=0.1] [N=64]          cavite"
	@echo "make figures                          figures a partir de results/"
	@echo "make all                              q1 q2 q3 q4 figures"
	@echo "make clean                            supprime results/ et figures/"

all: q1 q2 q3 q4 figures

q1: N ?= 16
q1:
	@mkdir -p results/q1
	$(RUN) src/q1_validation.edp -k $(K) -n $(N) | tee results/q1/freefem_P$(K).txt

q2: q2-k2 q2-k3

q2-k2 q2-k3: NMIN ?= 4
q2-k2 q2-k3: NMAX ?= 128
q2-k2 q2-k3:
	@mkdir -p results/q2
	$(RUN) src/q2_convergence.edp -k $(subst q2-k,,$@) -nmin $(NMIN) -nmax $(NMAX) | tee results/q2/freefem_P$(subst q2-k,,$@).txt

q3: NMIN ?= 8
q3: NMAX ?= 64
q3:
	@mkdir -p results/q3
	$(RUN) src/q3_viscosity.edp -nmin $(NMIN) -nmax $(NMAX) | tee results/q3/freefem_P2.txt

q4: N ?= 64
q4:
	@mkdir -p results/q4
	$(RUN) src/q4_cavity.edp -nu $(NU) -n $(N) | tee results/q4/freefem_nu$(NU).txt

figures:
	$(PY) scripts/plots.py

clean:
	rm -rf results figures
