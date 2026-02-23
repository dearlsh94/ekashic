# Work Development Rules

## 🏛️ Architecture & System Design
- **Strategic Abstraction**: Prioritize clear interfaces and maintainability. Avoid over-engineering, but ensure logic is decoupled for future scaling.
- **Poly-repo Awareness**: Always consider the impact on interdependent services. Check repository dependencies before proposing structural changes.

## 🛠️ Implementation Standards
- **Standardized Contexts**: Strictly adhere to the architecture and patterns defined in `kos-frontend-contexts` and `connect-frontend-contexts`.
- **Marketplace First**: Prioritize utilizing internal Marketplace skills and shared tools to maintain consistency.
- **Security & Reliability**: Never hardcode credentials. Use designated secret managers. Ensure critical logic is backed by unit tests.
- **Clean Comments**: Avoid unnecessary comments that merely restate the code implementation. Comments should provide context, reasoning, or explain complex business logic, not describe what the code obviously does.

## 📝 Living Docs (Knowledge Sync)
- **Systematic Planning**: Use "Plan Mode" to visualize architectural impacts before execution.
