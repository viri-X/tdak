# Contributing to TDAK

Welcome! As a mathematical physicist exploring algebraic topology in Kubernetes networks, I’m excited to collaborate.  
Your feedback, bug reports, and ideas are invaluable at this early stage.

---

## How to Contribute

### 1. Reporting Bugs or Ideas
- **Open an Issue**: Describe the problem or suggestion in [GitHub Issues](https://github.com/viri-X/tdak/issues).
- For bugs, include:
  - Error logs
  - Steps to reproduce
  - A minimal example (if possible)

### 2. Code Contributions
1. **Fork the repository**.
2. **Set up locally**:
   ```bash
   git clone https://github.com/viri-X/tdak.git
   cd tdak
   pip install -r requirements.txt
   ```
3. **Create a branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Test your changes:**
   ```bash
   pytest tests/  # Ensure existing tests pass
   ```
5. **Submit a Pull Request (PR):** Link it to an existing issue (if applicable).

### 3. Feature Requests
- Open an issue with the "enhancement" label.

- Explain:

  -The problem you’re solving (e.g., "Detect slow network partitions using persistent homology")

  -How it aligns with TDAK’s goal: bridging abstract topology and cloud infrastructure

###4. Questions or Discussions
-Start a GitHub Discussion for open-ended ideas.

-Example topics:

  -"How to visualize topological features in Kubernetes?"

  -"Could Morse theory improve failure detection?"

## Code Guidelines
-Documentation: Update docs/TDAK_DOCUMENTATION.md if your change affects functionality.

-Tests: Add tests in tests/ for new features.

-Style: Follow PEP8 (Python) and comment complex topological logic.

## First-Time Contributors
New to GitHub? Check out [GitHub’s PR Guide](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).

This project adheres to a Code of Conduct. [![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md).



