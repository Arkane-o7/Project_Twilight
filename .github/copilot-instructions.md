# Project Twilight - GitHub Copilot Instructions

**ALWAYS follow these instructions first** and only fallback to additional search and context gathering if the information in the instructions is incomplete or found to be in error.

## Repository Overview
Project Twilight is currently a minimal repository containing only basic documentation. This repository serves as a foundation for future development and contains the essential setup for GitHub workflows and documentation.

## Working Effectively

### Essential Prerequisites
Before working on any changes, verify your environment has the required tools:
- Git is available at `/usr/bin/git` (version 2.51.0+)
- Node.js is available at `/usr/local/bin/node` (version 20.19.5+)
- npm is available at `/usr/local/bin/npm` (version 10.8.2+)
- Python3 is available at `/usr/bin/python3` (version 3.12.3+)
- Docker is available at `/usr/bin/docker` (version 28.0.4+)

### Initial Repository Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Arkane-o7/Project_Twilight.git
   cd Project_Twilight
   ```

2. Verify the repository state:
   ```bash
   git status
   ls -la
   ```
   - Expected execution time: < 1 second
   - Should show clean working tree with README.md and .github/ directory

### Current Repository Structure
```
Project_Twilight/
├── .git/                    # Git repository metadata
├── .github/                 # GitHub workflows and configurations
│   └── copilot-instructions.md  # This file
└── README.md               # Basic project documentation
```

### Development Workflow

#### Making Changes
1. **ALWAYS** create a new branch for changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **ALWAYS** check the current repository state before making changes:
   ```bash
   git status
   git branch
   ```

3. Make your changes using appropriate tools and follow the existing code style

4. **ALWAYS** commit changes with descriptive messages:
   ```bash
   git add .
   git commit -m "Descriptive commit message"
   ```

5. Push changes and create pull requests:
   ```bash
   git push origin feature/your-feature-name
   ```

#### Testing Changes
Currently, there are no automated tests in the repository. When adding code:
- **ALWAYS** manually test any new functionality
- **ALWAYS** verify that changes work as expected
- **ALWAYS** ensure documentation is updated to reflect changes

### Common Development Tasks

#### Documentation Updates
- Edit README.md for project-level documentation
- Add new documentation files in markdown format
- **ALWAYS** use consistent markdown formatting
- Expected time for documentation changes: < 30 seconds

#### Adding New Features
When adding new code to this repository:

1. **ALWAYS** determine the appropriate project structure first
2. **ALWAYS** add appropriate build configuration (package.json, requirements.txt, etc.)
3. **ALWAYS** include documentation for any new functionality
4. **ALWAYS** test the complete workflow from fresh clone to running application

#### Setting Up Build Systems
When adding build systems to this repository:

**For Node.js projects:**
```bash
npm init -y
npm install [dependencies]
npm run build  # Configure in package.json - NEVER CANCEL, may take 5-45 minutes
npm test       # Configure in package.json - NEVER CANCEL, may take 2-15 minutes
```

**For Python projects:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m pytest  # NEVER CANCEL, may take 2-15 minutes
```

**For Docker projects:**
```bash
docker build -t project-twilight .  # NEVER CANCEL, may take 5-30 minutes
docker run project-twilight
```

### Critical Build and Test Guidelines

#### Timeout Settings
- **NEVER CANCEL** any build or test commands
- **ALWAYS** set timeouts of 60+ minutes for build commands
- **ALWAYS** set timeouts of 30+ minutes for test commands
- If a command appears to hang, wait at least 60 minutes before considering alternatives

#### Expected Timing
- Git operations: < 5 seconds
- File operations: < 5 seconds
- Documentation changes: < 30 seconds
- Future build operations: 5-45 minutes (when build system is added)
- Future test operations: 2-15 minutes (when tests are added)

### Validation Requirements

#### Before Committing Changes
1. **ALWAYS** verify the repository is in a clean state:
   ```bash
   git status
   ```

2. **ALWAYS** check that all files are properly tracked:
   ```bash
   git ls-files
   ```

3. **ALWAYS** ensure no unintended files are committed:
   ```bash
   git diff --cached
   ```

#### Manual Testing Scenarios
Since this is currently a minimal repository, manual testing consists of:

1. **Repository integrity test:**
   - Clone repository fresh
   - Verify all expected files are present
   - Ensure README.md is readable and accurate

2. **Future application testing** (when code is added):
   - **ALWAYS** test the complete user workflow from installation to usage
   - **ALWAYS** verify that the application starts successfully
   - **ALWAYS** execute at least one end-to-end scenario
   - **ALWAYS** take screenshots of UI changes (when applicable)

### Common Troubleshooting

#### Git Issues
- If branch conflicts occur, coordinate with repository maintainers
- Use `git status` to understand current state
- Use `git log --oneline -10` to see recent commits

#### Environment Issues
- Verify all prerequisite tools are installed and accessible
- Check PATH environment variable if commands are not found
- Use absolute paths when relative paths fail

### Repository Maintenance

#### Adding CI/CD
When adding GitHub Actions workflows:
1. Create `.github/workflows/` directory
2. Add workflow YAML files with appropriate timeouts
3. **ALWAYS** test workflows in feature branches first
4. **NEVER CANCEL** workflow runs, even if they take 45+ minutes

#### Code Quality
When adding linting and formatting:
1. Add configuration files (.eslintrc, .prettierrc, etc.)
2. Add npm scripts or equivalent for easy execution
3. **ALWAYS** run linting before committing: `npm run lint`
4. **ALWAYS** run formatting before committing: `npm run format`

## Key Repository Information

### Current State
- **Language:** Documentation only (Markdown)
- **Build System:** None (to be added)
- **Test Framework:** None (to be added)
- **CI/CD:** None (to be added)
- **Dependencies:** None (to be added)

### Future Development Considerations
This repository is set up for expansion. When adding new functionality:
- Choose appropriate language and framework
- Add proper build and test infrastructure
- Update these instructions with specific build/test commands
- Include proper validation scenarios

### Important Notes
- This repository is currently in early development phase
- Build and test instructions will be updated as the project grows
- **ALWAYS** refer to the most recent version of these instructions
- **ALWAYS** update these instructions when adding new build or test processes