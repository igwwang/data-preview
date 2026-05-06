# Naming Conventions Guide

This document defines the naming conventions for files, directories, and documentation in our project to ensure consistency across the team.

## File Naming Conventions

### 1. Documentation Files

#### Format

- Use **kebab-case** for all documentation files
- Use lowercase letters only
- Separate words with hyphens (`-`)
- Use descriptive, business-focused names

#### Examples

```
✅ Good
device-group-data.md
device-update-check.md
protocol-agreement.md
user-consent-management.md
api-integration-guide.md

❌ Bad
DeviceGroupData.md          # PascalCase
device_group_data.md        # snake_case
devicegroupdata.md          # no separators
Device Group Data.md        # spaces
DataController.md           # implementation details
```



### 2. API Documentation Files

#### Naming Strategy

Name files based on **business functionality**, not implementation details:

```
✅ Business-focused naming
device-group-data.md       # What it does: queries device group data
device-update-check.md     # What it does: checks for updates
protocol-agreement.md      # What it does: handles agreement

❌ Implementation-focused naming
data-controller.md         # How it's implemented
device-update-controller.md # Technical implementation
tou-agree-controller.md    # Code structure
```

### 3. Standards Files

```
✅ Standards naming
PROJECT-README-TEMPLATE.md
API-DOC-STANDARDS.md
PROJECT-STRUCTURE-TEMPLATE.md
NAMING-CONVENTIONS.md
TASK-DOC-STANDARDS.md
```

### 4. Configuration Files

```
✅ Configuration files
docker-compose.yml
application-dev.yml
logback-spring.xml
```

## Directory Naming Conventions

### 1. Documentation Directories

```
docs/
├── api/                   # API documentation
├── architecture/          # Architecture documents
├── deployment/            # Deployment guides
├── development/           # Development guides
├── examples/              # Code examples
└── standards/             # Documentation standards
```

### 2. Source Code Directories

Follow Java package naming conventions:

```
src/main/java/com/wtv/project/
├── controller/            # REST controllers
├── service/              # Business services
├── dao/                  # Data access objects
├── model/                # Data models
├── config/               # Configuration classes
└── util/                 # Utility classes
```

## Document Title Conventions

### 1. API Documentation Titles

#### Format

Use business-focused, user-friendly titles:

```
✅ Recommended titles
# Device Group Data Query API
# Device Update Check API
# Protocol Agreement API
# User Consent Management API

❌ Avoid implementation details
# DataController.getTouGroupData API Implementation Logic
# DeviceUpdateController.getDeviceUpdate Method Documentation
# TouAgreeController.agreeTou Technical Specification
```



### 2. Section Headers

Use consistent section naming:

```
✅ Standard sections
## API Overview
## Request Parameters
## Complete Implementation Logic
## Examples
## Data Source Architecture
## Business Logic Characteristics
## Exception Handling
## Performance Optimization Points
## Client Integration Guide
```

## URL and Endpoint Conventions

### 1. API Endpoints

```
✅ RESTful naming
GET  /device/group         # Resource-based
GET  /device/update        # Action-based when appropriate
PUT  /tou/agree           # Action-based for operations
POST /cmp/qrcode/generate # Nested resources
```

### 2. Documentation URLs

```
✅ URL-friendly paths
/docs/api/device-group-data
/docs/api/device-update-check
/docs/api/protocol-agreement

❌ Avoid
/docs/api/Device%20Group%20Data
/docs/api/DataController
/docs/api/device_group_data
```

## Variable and Parameter Naming

### 1. API Parameters

```
✅ Clear, descriptive names
deviceId                   # Clear purpose
consumerId                # Clear purpose
groupId                   # Clear purpose
langcode                  # Standard abbreviation
supportCmp                # Boolean flag

❌ Avoid
id                        # Too generic
data                      # Too vague
param1                    # Non-descriptive
```

### 2. Response Fields

```
✅ Consistent naming
{
  "error": 0,
  "timestemp": 1694163126736,
  "data": {
    "groupId": "...",
    "groupName": "...",
    "releaseTime": 1693916512302
  }
}
```

## Best Practices Summary

### 1. General Principles

- **Consistency**: Use the same naming pattern throughout the project
- **Clarity**: Names should clearly indicate purpose or content
- **Simplicity**: Avoid unnecessary complexity
- **Future-proof**: Consider how names will scale with project growth

### 2. File Organization

```
✅ Logical grouping
docs/
├── api/
│   ├── device-group-data.md
│   └── device-update-check.md
├── standards/
│   ├── API-DOC-STANDARDS.md
│   ├── NAMING-CONVENTIONS.md
│   └── PROJECT-README-TEMPLATE.md
└── architecture/
    ├── system-overview.md
    └── data-flow-design.md
```

### 3. Maintenance Guidelines

- Update this document when adding new naming patterns
- Review file names during code reviews
- Refactor inconsistent names when found
- Document exceptions with clear reasoning

## Tools and Automation

### 1. File Validation

Consider using tools to validate naming conventions:

```bash
# Example validation script
find docs/ -name "*.md" | grep -E "[A-Z]|_" | grep -v "_CN.md$"
```

### 2. IDE Configuration

Configure your IDE to suggest kebab-case for new files:

- VS Code: Use file templates
- IntelliJ: Configure file naming patterns

## Migration Guide

### 1. Existing Files

When renaming existing files:

1. Update all internal links
2. Update README references
3. Update build scripts if applicable
4. Communicate changes to team

### 2. Git History

```bash
# Preserve git history when renaming
git mv OldFileName.md new-file-name.md
```

## Examples by Category

### 1. API Documentation

```
device-group-data.md           # GET /device/group
device-update-check.md         # GET /device/update
protocol-agreement.md          # PUT /tou/agree

# Multi-method endpoints - separate controller methods
user-tcmap-get.md              # GET /user/tcmap (separate method)
user-tcmap-set.md              # POST /user/tcmap (separate method)

# Multi-method endpoints - single controller method
resource-management.md         # GET/POST /resource (single method)
```

### 2. Architecture Documentation

```
system-architecture.md         # Overall system design
database-design.md             # Database schema
security-design.md             # Security architecture
data-flow-diagram.md           # Data flow documentation
```

### 3. Deployment Documentation

```
deployment-guide.md            # General deployment
environment-setup.md           # Environment configuration
docker-deployment.md           # Docker specific
kubernetes-deployment.md       # K8s specific
```

### 4. Development Documentation

```
development-setup.md           # Dev environment setup
coding-standards.md            # Code style guide
testing-guide.md               # Testing procedures
api-integration-guide.md       # How to integrate APIs
troubleshooting-guide.md       # Common issues
```

### 5. Documentation Files

```
README.md                      # Project root README (main navigation)
docs/api/[api-name].md         # Individual API documentation
docs/api/[group]/[api-name].md # Grouped API documentation
docs/standards/[standard].md   # Documentation standards
```

---

**Document Version**: v1.0
**Last Updated**: 2025
**Applies To**: All project documentation and file naming

## Directory Organization

### Simple Structure

- **docs/**: Documentation root directory
- **docs/api/**: Individual API documentation files
- **docs/api/[group]/**: Grouped API files (no README needed)
- **docs/standards/**: Documentation standards
- **docs/architecture/**: Architecture documentation
- **docs/deployment/**: Deployment guides

## Document Cross-Reference

- Keep cross-references simple and minimal

## Checklist for New Files

- [ ]  File name uses kebab-case
- [ ]  Descriptive, business-focused naming
- [ ]  File placed in appropriate directory
