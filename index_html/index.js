const output = document.getElementById("output");
let n = 5;
let m = 3;

async function loadEnvironment() {
    const pyodide = await loadPyodide();
    await pyodide.loadPackage(['micropip']);
    await pyodide.runPythonAsync(`
        import micropip
        await micropip.install('symplexmethod-0.1.0-py3-none-any.whl')
    `);
    await pyodide.setStdout({
        batched: (s) => output.value += s + "\n",
    })
    output.value += "Ready!\n";
    return pyodide;
}

const pyodideReadyPromise = loadEnvironment();

async function solveSymplex() {
    const pyodide = await pyodideReadyPromise;
    try {
        const result = await pyodide.runPythonAsync(`
          from symplexmethod import solve
          solve([0, 1, -3, 0, 2, 0], [
          [1, 3, -1, 0, 2, 0],
          [0, -2, 4, 1, 0, 0],
          [0, -4, 3, 0, 8, 1]
          ], [7, 12, 10])
      `);
        console.log(result)
    } catch (err) {
        console.log(err);
    }
}

function changeN(delta) {
    n = Math.max(1, n + delta);
    createMatrixInputs();
}

function changeM(delta) {
    m = Math.max(1, m + delta);
    createMatrixInputs();
}

function parseMatrixA() {
    const matrix = [];
    for (let i = 0; i < m; i++) {
        const row = [];
        for (let j = 0; j < n; j++) {
            const value = document.getElementById(`a-cell-${i}-${j}`).value;
            row.push(value ? parseFloat(value) : 0);
        }
        matrix.push(row);
    }
    return matrix;
}

function parseMatrixB() {
    const matrix = [];
    for (let i = 0; i < n; i++) {
        const value = document.getElementById(`b-cell-${i}`).value;
        matrix.push(value ? parseFloat(value) : 0);
    }
    console.log(matrix)
}

function parseMatrixC() {
    const matrix = [];
    for (let i = 0; i < m; i++) {
        const value = document.getElementById(`c-cell-${i}`).value;
        matrix.push(value ? parseFloat(value) : 0);
    }
    console.log(matrix)
}


function createMatrixInputs() {
    const b_container = document.getElementById("b-matrix-container");
    b_container.innerHTML = '';
    b_container.style.gridTemplateColumns = `repeat(${n}, auto)`;
    for (let i = 0; i < n; i++) {
        const input = document.createElement("input");
        input.value = 0;
        input.type = "number";
        input.id = `b-cell-${i}`;
        b_container.appendChild(input);
    }

    const a_container = document.getElementById("a-matrix-container");
    a_container.innerHTML = '';
    a_container.style.gridTemplateColumns = `repeat(${n}, auto)`;

    for (let i = 0; i < m; i++) {
        for (let j = 0; j < n; j++) {
            const input = document.createElement("input");
            input.value = 0;
            input.type = "number";
            input.id = `a-cell-${i}-${j}`;
            a_container.appendChild(input);
        }
    }

    const c_container = document.getElementById("c-matrix-container");
    c_container.innerHTML = '';
    c_container.style.gridTemplateColumns = `repeat(${m}, auto)`;

    for (let i = 0; i < m; i++) {
        const input = document.createElement("input");
        input.value = 0;
        input.type = "number";
        input.id = `c-cell-${i}`;
        c_container.appendChild(input);
    }
}

createMatrixInputs()