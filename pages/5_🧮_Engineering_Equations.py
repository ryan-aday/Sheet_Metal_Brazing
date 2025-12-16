from typing import Dict, Optional

import pandas as pd
import streamlit as st
import sympy as sp

from app_data import EngineeringEquation, EQUATIONS

st.title("Sheet Metal Engineering Equations")

st.markdown(
    """
    Input known values for any equation and choose the variable to solve. Values are interpreted as
    floats; units are indicated for clarity. The solver uses Sympy and returns physically meaningful
    roots (real numbers). Equations are provided as reminders—validate against detailed design
    references and safety factors.
    """
)


def solve_equation(eq: EngineeringEquation, solve_for: str, inputs: Dict[str, Optional[float]]):
    symbols = {name: sp.symbols(name) for name in eq.variables.keys()}
    expression = sp.sympify(eq.expression, locals=symbols)
    equation = sp.Eq(expression, 0)

    substitutions = {symbols[k]: v for k, v in inputs.items() if v is not None and k != solve_for}
    target = symbols[solve_for]

    if len(substitutions) + 1 != len(symbols):
        missing = [k for k in eq.variables.keys() if k not in inputs or inputs[k] is None][0]
        raise ValueError(f"Provide all other values before solving (missing: {missing})")

    solved = sp.solve(equation.subs(substitutions), target)
    real_solutions = [s for s in solved if s.is_real]
    return real_solutions


for eq in EQUATIONS:
    with st.expander(eq.name, expanded=False):
        st.latex(sp.Eq(sp.sympify(eq.expression), 0))
        st.markdown("**Variables**")
        st.table(pd.DataFrame(list(eq.variables.items()), columns=["Symbol", "Meaning"]))

        solve_for = st.selectbox(
            "Select variable to solve for",
            options=list(eq.variables.keys()),
            key=f"solve_for_{eq.name}",
        )

        inputs: Dict[str, Optional[float]] = {}
        for symbol, meaning in eq.variables.items():
            if symbol == solve_for:
                inputs[symbol] = None
                continue
            inputs[symbol] = st.number_input(
                f"{symbol} — {meaning}",
                key=f"input_{eq.name}_{symbol}",
                value=0.0,
                format="%.6f",
            )

        if st.button("Solve", key=f"solve_button_{eq.name}"):
            try:
                solutions = solve_equation(eq, solve_for, inputs)
                if not solutions:
                    st.warning("No real solutions found with the provided values.")
                else:
                    st.success(f"Solutions for {solve_for}: {', '.join(str(s) for s in solutions)}")
            except Exception as exc:  # noqa: BLE001
                st.error(str(exc))
