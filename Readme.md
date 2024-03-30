# Readme

Rest interface to the solvespace CAD constraint solver.
It is assumed that the following python extension is installed:
https://github.com/sg-dev1/solvespace_python

## Installation

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the virtual environment

- On Windows:

```bash
venv\Scripts\activate
```

- On macOS and Linux:

```bash
source venv/bin/activate
```

### Install the required packages

```bash
pip install -r requirements.txt
```

## Dataformat for /solve POST endpoint

```ts
export interface SolverRequestType {
  workplane: string;
  entities: { id: number; t: 'point' | 'line' | 'circle' | 'arc'; v: number[] }[];
  constraints: { id: number; t: SlvsConstraints; v: number[] }[];
}

export interface SolverResponseType {
  code: number;
  failed: number[];
  entities: { id: number; t: 'point' | 'line' | 'circle' | 'arc'; v: number[] }[];
  dof: number;
}
```
