# Checking Xcode Cloud CI Status via GitHub MCP

This skill uses the GitHub CLI to check Xcode Cloud build status for iOS projects.

## Prerequisites

- GitHub CLI (`gh`) authenticated
- Repository with Xcode Cloud integration configured

## Checking CI Status

### Quick Status Check

Use `gh pr checks` to see a summary of CI status for a pull request:

```bash
gh pr checks <PR_NUMBER> --repo <owner>/<repo>
```

Example output:
```
Some checks were not successful
0 cancelled, 2 failing, 0 successful, 0 skipped, and 0 pending checks

   NAME                         DESCRIPTION  ELAPSED  URL                       
X  tankgameBT | PR Build        failed                https://appstoreconnect...
X  tankgameBT | PR Build | ...               44s      https://appstoreconnect...
```

### Detailed Build Errors and Warnings

To get detailed error/warning information from Xcode Cloud builds:

```bash
# Get the head commit SHA for the PR
HEAD_SHA=$(gh pr view <PR_NUMBER> --repo <owner>/<repo> --json headRefOid -q '.headRefOid')

# Get check run details with build output
gh api repos/<owner>/<repo>/commits/${HEAD_SHA}/check-runs \
  --jq '.check_runs[] | {name: .name, status: .status, conclusion: .conclusion, output: .output}'
```

### Understanding the Output

The check run output includes:
- **status**: `queued`, `in_progress`, or `completed`
- **conclusion**: `success`, `failure`, `action_required`, `cancelled`, `skipped`, `timed_out`
- **output.summary**: Build metrics table (errors, warnings, test failures, analysis issues)
- **output.text**: Detailed error/warning messages with descriptions

Example output structure:
```json
{
  "name": "tankgameBT | PR Build | Build - iOS",
  "status": "completed",
  "conclusion": "action_required",
  "output": {
    "annotations_count": 0,
    "summary": "|Report Summary||\n|-------------|-------------|\n|Errors|2|\n|Test Failures|0|\n|Analysis Issues|0|\n|Warnings|0|\n",
    "text": "## 2 Errors \n<details>...</details>",
    "title": "2 errors"
  }
}
```

### Common Xcode Cloud Check Names

Xcode Cloud checks typically follow this naming pattern:
- `<ProductName> | <WorkflowName>` - Parent workflow status
- `<ProductName> | <WorkflowName> | Build - iOS` - iOS build action
- `<ProductName> | <WorkflowName> | Test - iOS` - Test action (if configured)

Example: `tankgameBT | PR Build | Build - iOS`

## Workflow Integration

When asked to check CI status on an iOS project:

1. **Identify the PR or branch** to check
2. **Run quick status check** with `gh pr checks`
3. **Get detailed errors/warnings** if needed using the check-runs API
4. **Report findings** including:
   - Overall status (passing/failing)
   - Number of errors, warnings, test failures
   - Specific error messages from build output

## Troubleshooting Common Errors

### Swift Package Manager Resolution
If you see errors about `Package.resolved`:
```
a resolved file is required when automatic dependency resolution is disabled
```
**Fix**: Commit the `Package.resolved` file to the repository.

### Code Signing
Xcode Cloud handles code signing automatically, but ensure:
- App Store Connect is properly linked
- Required certificates/profiles are available in the Apple Developer portal

### Missing Dependencies
Ensure all SPM dependencies are accessible (public repos or configured credentials).
