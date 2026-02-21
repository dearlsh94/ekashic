# Work Development Rules

## 🏛️ Architecture & System Design
- **Strategic Abstraction**: Prioritize clear interfaces and maintainability. Avoid over-engineering, but ensure logic is decoupled for future scaling.
- **Poly-repo Awareness**: Always consider the impact on interdependent services. Check repository dependencies before proposing structural changes.

## 🛠️ Implementation Standards
- **Marketplace First**: Prioritize utilizing internal Marketplace skills and shared tools to maintain consistency.
- **Security & Reliability**: Never hardcode credentials. Use designated secret managers. Ensure critical logic is backed by unit tests.

## 📝 Living Docs (Knowledge Sync)
- **Systematic Planning**: Use "Plan Mode" to visualize architectural impacts before execution.
