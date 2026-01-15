# Contributing to Wyckoff Trading Method Bot

Thank you for your interest in contributing to the Wyckoff Trading Method Bot! This document provides guidelines for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How Can I Contribute?](#how-can-i-contribute)
3. [Development Setup](#development-setup)
4. [Coding Standards](#coding-standards)
5. [Testing Guidelines](#testing-guidelines)
6. [Submitting Changes](#submitting-changes)
7. [Bug Reports](#bug-reports)
8. [Feature Requests](#feature-requests)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in all interactions.

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behavior includes:**
- Harassment, trolling, or insulting/derogatory comments
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

## How Can I Contribute?

### Reporting Bugs

Before submitting a bug report:
1. Check the [FAQ](FAQ.md) for common issues
2. Search existing issues to avoid duplicates
3. Test on the latest version
4. Try to reproduce on a demo account

When submitting a bug report, include:
- **Title**: Clear, descriptive title
- **Description**: Detailed description of the issue
- **Steps to Reproduce**: Step-by-step instructions
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Environment**:
  - MT5 version and build number
  - Operating system
  - Symbol and timeframe
  - Parameter settings used
- **Logs**: Relevant excerpts from Experts log
- **Screenshots**: If applicable

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:
- **Use Case**: Why this enhancement would be useful
- **Proposed Solution**: Your suggested implementation
- **Alternatives**: Other approaches you've considered
- **Impact**: How this affects existing functionality

### Code Contributions

Areas where contributions are particularly welcome:
- Additional Wyckoff patterns (LPS, Backup Action, etc.)
- Multi-timeframe analysis
- Performance optimizations
- Documentation improvements
- Bug fixes
- Test coverage improvements

## Development Setup

### Prerequisites

1. **MetaTrader 5**: Latest version installed
2. **MetaEditor**: Comes with MT5
3. **Git**: For version control
4. **Demo Account**: For testing

### Setting Up Development Environment

1. **Fork the Repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/Wyckoff-Trading-Method-.git
   cd Wyckoff-Trading-Method-
   ```

2. **Create Development Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b bugfix/issue-description
   ```

3. **Install Files in MT5**
   - Copy files to MT5 data folder
   - Compile in MetaEditor
   - Test on demo account

### Development Workflow

```
1. Create branch from main
2. Make changes
3. Test thoroughly
4. Commit with clear messages
5. Push to your fork
6. Create Pull Request
```

## Coding Standards

### MQL5 Code Style

**Naming Conventions:**
```mql5
// Classes: PascalCase with 'C' prefix
class CWyckoffAnalysis { };

// Functions: PascalCase
void AnalyzeMarket() { }

// Variables: camelCase
int barCount = 0;

// Constants: UPPER_SNAKE_CASE
#define MAX_BARS 1000

// Member variables: camelCase with 'm_' prefix
int m_volumePeriod;

// Input parameters: PascalCase
input int VolumePeriod = 20;
```

**Code Organization:**
```mql5
//+------------------------------------------------------------------+
//| Function description                                              |
//+------------------------------------------------------------------+
ReturnType FunctionName(parameters)
{
    //--- Section comment
    code here;
    
    //--- Another section
    more code;
    
    return value;
}
```

**Best Practices:**
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and small
- Handle errors gracefully
- Use const where appropriate
- Initialize all variables
- Check array bounds
- Validate input parameters

### Documentation Standards

**Code Comments:**
```mql5
//--- Single line comment for simple explanations

/*
  Multi-line comment for
  more complex explanations
*/

//+------------------------------------------------------------------+
//| Header comment for major sections                                |
//+------------------------------------------------------------------+
```

**Function Documentation:**
```mql5
//+------------------------------------------------------------------+
//| Calculate position size based on risk                             |
//| Parameters:                                                       |
//|   stopLossDistance - Distance to stop loss in price units        |
//| Returns:                                                          |
//|   Calculated lot size normalized to broker requirements          |
//+------------------------------------------------------------------+
double CalculateLotSize(double stopLossDistance)
{
    // Implementation
}
```

**Markdown Documentation:**
- Use clear headings
- Include code examples
- Add tables for comparisons
- Use bullet points for lists
- Include warnings where appropriate

## Testing Guidelines

### Before Submitting Code

**Required Tests:**

1. **Compilation Test**
   ```
   - Open MetaEditor
   - Compile with 0 errors, 0 warnings
   - Check all dependencies resolve
   ```

2. **Strategy Tester**
   ```
   - Test on at least 1 year of data
   - Test on multiple symbols (3+)
   - Test on multiple timeframes (2+)
   - Verify no crashes or errors
   - Check log for warnings
   ```

3. **Demo Account Testing**
   ```
   - Run for minimum 1 week
   - Monitor for errors in Experts log
   - Verify trades execute correctly
   - Check position sizing works
   - Confirm stops and targets set properly
   ```

4. **Edge Cases**
   ```
   - Low liquidity periods
   - High spread conditions
   - Market gaps (weekends)
   - Low margin situations
   - Connection interruptions
   ```

### Test Checklist

- [ ] Code compiles without errors or warnings
- [ ] Backtests complete successfully
- [ ] No memory leaks (long backtests)
- [ ] Works on H1 and H4 timeframes
- [ ] Tested on EURUSD, GBPUSD, USDJPY
- [ ] Demo tested for 1+ week
- [ ] No errors in Experts log
- [ ] Existing functionality not broken
- [ ] Documentation updated
- [ ] Comments added for complex code

## Submitting Changes

### Pull Request Process

1. **Update Documentation**
   - Update README.md if needed
   - Update relevant guides
   - Add to CHANGELOG.md
   - Update version if applicable

2. **Create Pull Request**
   - Use clear, descriptive title
   - Reference related issues (#123)
   - Describe changes made
   - List testing performed
   - Note any breaking changes

3. **PR Description Template**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update
   
   ## Testing
   - Describe testing performed
   - Include test results
   
   ## Checklist
   - [ ] Code compiles without errors
   - [ ] Tested on demo account
   - [ ] Documentation updated
   - [ ] CHANGELOG.md updated
   ```

4. **Review Process**
   - Maintainers will review your PR
   - Address feedback and comments
   - Make requested changes
   - PR will be merged when approved

### Commit Message Guidelines

**Format:**
```
type(scope): brief description

Longer description if needed explaining:
- Why the change was made
- What problem it solves
- Any side effects

Closes #123
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, no code change
- `refactor`: Code change without behavior change
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(analysis): add Last Point of Support detection

Implements LPS pattern recognition to identify optimal entry
points after spring events. Improves accuracy of buy signals.

fix(position): correct lot size calculation for JPY pairs

The tick value calculation was incorrect for JPY pairs due to
different quote currency. Now uses proper conversion.

docs(readme): add troubleshooting section

Added common issues and solutions based on user feedback.
```

## Bug Reports

### Bug Report Template

```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Step one
2. Step two
3. Step three

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- MT5 Version: [e.g., Build 3850]
- OS: [e.g., Windows 11]
- Symbol: [e.g., EURUSD]
- Timeframe: [e.g., H1]
- EA Version: [e.g., 1.0.0]

**Settings**
- RiskPercent: [value]
- AccumulationBars: [value]
- Other relevant settings

**Logs**
```
Paste relevant log excerpts here
```

**Screenshots**
If applicable, add screenshots
```

## Feature Requests

### Feature Request Template

```markdown
**Feature Description**
Clear description of the proposed feature

**Use Case**
Why this feature would be useful

**Proposed Implementation**
How you think it should work

**Alternatives Considered**
Other approaches you've thought about

**Additional Context**
Any other relevant information
```

## Code Review Criteria

When reviewing PRs, we consider:

**Functionality:**
- Does it work as intended?
- Are edge cases handled?
- Is error handling adequate?

**Code Quality:**
- Follows coding standards?
- Well-commented and documented?
- No unnecessary complexity?
- Efficient implementation?

**Testing:**
- Adequate test coverage?
- Tested on demo account?
- Backtested on historical data?

**Documentation:**
- User-facing docs updated?
- Code comments adequate?
- CHANGELOG updated?

**Compatibility:**
- Works on MT5 build 2600+?
- Compatible with existing features?
- No breaking changes (or documented)?

## Recognition

Contributors will be:
- Listed in repository contributors
- Credited in CHANGELOG.md
- Thanked in release notes

Significant contributors may be invited to join as maintainers.

## Questions?

- Check the [FAQ](FAQ.md)
- Review [USER_GUIDE.md](USER_GUIDE.md)
- Open a discussion on GitHub
- Search existing issues

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to the Wyckoff Trading Method Bot!**

Your efforts help make algorithmic trading more accessible to everyone. Whether it's fixing a typo or implementing a major feature, every contribution is valued.

*Happy coding and profitable trading!* 📈
