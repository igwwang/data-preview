# Java Project Structure Template

This is a standard Java Spring Boot project structure template for enterprise application development.

## Complete Project Structure

```
[project-name]/                  # Project root directory
├── README.md                    # Main project documentation (English)
├── README.zh.md                 # Main project documentation (Chinese)
├── pom.xml                      # Maven build configuration
├── .gitignore                   # Git ignore file
├── .github/                     # GitHub configuration (optional)
│   ├── workflows/               # CI/CD workflows
│   │   ├── ci.yml              # Continuous integration config
│   │   └── cd.yml              # Continuous deployment config
│   ├── ISSUE_TEMPLATE/          # Issue templates
│   │   ├── bug_report.md        # Bug report template
│   │   └── feature_request.md   # Feature request template
│   └── pull_request_template.md # PR template
├── src/                         # Source code directory
│   ├── main/                    # Main source code
│   │   ├── java/                # Java source code
│   │   │   └── com/[company]/[project]/  # Package structure
│   │   │       ├── [ProjectName]Application.java  # Spring Boot main class
│   │   │       ├── controller/  # Controller layer
│   │   │       │   ├── BaseController.java         # Base controller class
│   │   │       │   ├── [Entity]Controller.java     # Entity controller
│   │   │       │   └── advice/  # Global exception handling
│   │   │       ├── service/     # Business logic layer
│   │   │       │   ├── [Entity]Service.java        # Service interface
│   │   │       │   └── impl/    # Implementation classes
│   │   │       ├── dao/         # Data access layer
│   │   │       │   ├── [Entity]Dao.java            # DAO interface
│   │   │       │   └── mapper/  # MyBatis mappers
│   │   │       ├── model/       # Data models
│   │   │       │   ├── entity/  # Entity classes
│   │   │       │   ├── dto/     # Data transfer objects
│   │   │       │   └── vo/      # View objects
│   │   │       ├── config/      # Configuration classes
│   │   │       │   ├── DatabaseConfig.java         # Database configuration
│   │   │       │   ├── RedisConfig.java            # Redis configuration
│   │   │       │   └── SecurityConfig.java         # Security configuration
│   │   │       ├── util/        # Utility classes
│   │   │       │   ├── DateUtils.java              # Date utility
│   │   │       │   └── JsonUtils.java              # JSON utility
│   │   │       ├── common/      # Common classes
│   │   │       │   ├── constants/  # Constants
│   │   │       │   ├── enums/      # Enumerations
│   │   │       │   └── result/     # Unified response results
│   │   │       └── exception/   # Custom exceptions
│   │   ├── resources/           # Resource files
│   │   │   ├── application.yml  # Main configuration file
│   │   │   ├── application-dev.yml   # Development environment config
│   │   │   ├── application-test.yml  # Test environment config
│   │   │   ├── application-prod.yml  # Production environment config
│   │   │   ├── logback-spring.xml    # Logging configuration
│   │   │   ├── mapper/          # MyBatis mapping files
│   │   │   ├── static/          # Static resources
│   │   │   │   ├── css/         # CSS files
│   │   │   │   ├── js/          # JavaScript files
│   │   │   │   └── images/      # Image files
│   │   │   └── templates/       # Template files
│   │   └── webapp/              # Web application resources (if needed)
│   │       ├── WEB-INF/         # Web application configuration
│   │       │   ├── web.xml      # Web configuration
│   │       │   └── templates/   # Web templates
│   │       └── static/          # Static web resources
│   ├── test/                    # Test code
│   │   ├── java/                # Test source code
│   │   │   └── com/[company]/[project]/  # Test package structure
│   │   │       ├── controller/  # Controller tests
│   │   │       │   └── [Entity]ControllerTest.java # Controller test class
│   │   │       ├── service/     # Service tests
│   │   │       │   └── [Entity]ServiceTest.java    # Service test class
│   │   │       ├── dao/         # Data access tests
│   │   │       └── integration/ # Integration tests
│   │   └── resources/           # Test resources
│   │       ├── application-test.yml                # Test configuration
│   │       └── test-data/       # Test data
│   └── site/                    # Maven Site documentation (optional)
│       ├── apt/                 # APT format documentation
│       ├── fml/                 # FAQ documentation
│       └── markdown/            # Markdown documentation
├── target/                      # Maven build output (Git ignored)
│   ├── classes/                 # Compiled classes
│   ├── test-classes/            # Compiled test classes
│   ├── site/                    # Generated documentation site
│   └── [project-name]-[version].jar  # Built JAR file
├── docs/                        # Project documentation
│   ├── releases/                # Version iteration documentation
│   │   ├── CHANGELOG.md         # Change log summary (optional)
│   │   ├── v1.0.0-design.md     # v1.0.0 complete version design document
│   │   ├── v1.1.0-design.md     # v1.1.0 complete version design document
│   │   ├── v1.2.0-design.md     # v1.2.0 complete version design document
│   │   └── v2.0.0-design.md     # v2.0.0 complete version design document
│   ├── api/                     # API design documentation (for API projects)
│   │   ├── [api-name].md        # API documentation (Chinese)
│   │   ├── [api-name]_EN.md     # API documentation (English)
│   │   └── openapi.yml          # OpenAPI specification (optional)
│   ├── tasks/                   # Task documentation (for task-based projects)
│   │   ├── data-ingestion.md    # Data ingestion task documentation
│   │   ├── data-processing.md   # Data processing task documentation
│   │   ├── data-cleanup.md      # Data cleanup task documentation
│   │   ├── data-sync.md         # Data synchronization task documentation
│   │   └── [task-name].md       # Individual task documentation
│   ├── operations/              # Operations documentation (for task-based projects)
│   │   ├── deployment.md        # Deployment guide
│   │   ├── monitoring.md        # Monitoring configuration
│   │   ├── troubleshooting.md   # Troubleshooting guide
│   │   └── maintenance.md       # Daily maintenance tasks
│   ├── data/                    # Data-related documentation (for task-based projects)
│   │   ├── sources.md           # Data source documentation
│   │   ├── formats.md           # Data format specifications
│   │   ├── quality.md           # Data quality standards
│   │   └── lineage.md           # Data lineage documentation
│   ├── architecture/            # Architecture documentation
│   │   ├── system-architecture.md    # System architecture design
│   │   ├── database-design.md        # Database design
│   │   ├── security-design.md        # Security design
│   │   ├── overview.md               # Architecture overview (for task-based projects)
│   │   ├── components.md             # Component documentation (for task-based projects)
│   │   ├── integration.md            # Integration documentation (for task-based projects)
│   │   └── images/              # Architecture diagrams
│   │       ├── system-overview.png   # System overview diagram
│   │       ├── data-flow.png         # Data flow diagram
│   │       └── task-dependencies.png # Task dependency diagram (for task-based projects)
│   ├── deployment/              # Deployment documentation
│   │   ├── deployment-guide.md       # Deployment guide
│   │   ├── environment-setup.md      # Environment setup
│   │   ├── docker/              # Docker related
│   │   │   ├── Dockerfile       # Docker image definition
│   │   │   ├── docker-compose.yml    # Docker compose config
│   │   │   └── docker-compose.prod.yml # Production docker compose
│   │   └── kubernetes/          # K8s configuration (if needed)
│   │       ├── deployment.yaml  # K8s deployment config
│   │       ├── service.yaml     # K8s service config
│   │       └── configmap.yaml   # K8s config map
│   ├── development/             # Development documentation
│   │   ├── setup-guide.md       # Development environment setup
│   │   ├── coding-standards.md  # Coding standards
│   │   ├── testing-guide.md     # Testing guide
│   │   └── database-migration.md # Database migration
│   ├── examples/                # Example code
│   │   ├── api-examples.md      # API usage examples (for API projects)
│   │   ├── curl-examples.sh     # cURL examples (for API projects)
│   │   ├── task-examples.md     # Task execution examples (for task-based projects)
│   │   ├── config-examples/     # Configuration examples (for task-based projects)
│   │   │   ├── scheduler.yml    # Scheduler configuration examples
│   │   │   └── datasource.yml   # Data source configuration examples
│   │   └── client-examples/     # Client examples
│   │       ├── java/            # Java client examples
│   │       ├── javascript/      # JavaScript client examples
│   │       └── python/          # Python client examples
│   └── standards/               # Documentation standards
│       ├── API-DOC-STANDARDS.md  # API documentation standards
│       ├── NAMING-CONVENTIONS.md # Naming conventions guide
│       ├── PROJECT-README-TEMPLATE.md   # README template (unified for API and task projects)
│       ├── PROJECT-STRUCTURE-TEMPLATE.md # Project structure template
│       └── TASK-DOC-STANDARDS.md # Task project documentation standards
├── scripts/                     # Script files
│   ├── build.sh                 # Build script
│   ├── deploy.sh                # Deployment script
│   ├── start.sh                 # Start script
│   ├── stop.sh                  # Stop script
│   └── database/                # Database scripts
│       ├── schema.sql           # Database schema
│       ├── data.sql             # Initial data
│       └── migration/           # Database migration scripts
├── config/                      # External configuration files
│   ├── dev/                     # Development environment config
│   │   ├── application.yml      # Development application config
│   │   └── logback.xml          # Development logging config
│   ├── test/                    # Test environment config
│   └── prod/                    # Production environment config
├── logs/                        # Log directory (Git ignored)
├── CHANGELOG.md                 # Change log
├── CONTRIBUTING.md              # Contributing guide
└── LICENSE                      # License file
```

## Usage Instructions

### 1. Creating a New Project
1. Copy this structure to your new project directory
2. Replace all placeholders like `[project-name]`, `[company]`, `[Entity]`, etc.
3. Remove unnecessary directories and files
4. Adjust structure according to project requirements

### 2. Placeholder Descriptions
- `[project-name]`: Project name, e.g., `user-service`
- `[company]`: Company domain, e.g., `wtv`
- `[Entity]`: Entity name, e.g., `User`, `Order`
- `[Controller]`: Controller name, e.g., `UserController`
- `[ProjectName]`: Project name in CamelCase, e.g., `UserService`

### 3. Directory Purpose

#### Core Source Code (`src/main/java`)
- **controller**: REST API controllers
- **service**: Business logic layer
- **dao**: Data access layer
- **model**: Data models (entity/dto/vo)
- **config**: Spring configuration classes
- **util**: Utility classes
- **common**: Common components
- **exception**: Custom exceptions

#### Test Code (`src/test/java`)
- **controller**: Controller unit tests
- **service**: Service layer unit tests
- **dao**: Data access layer tests
- **integration**: Integration tests

#### Documentation Structure (`docs/`)

**For API Projects**:
- **api**: API technical documentation
- **examples**: API usage examples and client code

**For Task-Based Projects**:
- **tasks**: Individual task documentation
- **operations**: Deployment, monitoring, and troubleshooting guides
- **data**: Data source, format, and quality documentation

**Common for All Projects**:
- **architecture**: System architecture design
- **deployment**: Deployment and operations documentation
- **development**: Developer guides
- **examples**: Usage examples
- **standards**: Documentation standards

#### Configuration and Scripts
- **config**: Environment-specific configurations
- **scripts**: Automation scripts
- **docker**: Containerization configurations

### 4. Best Practices

#### Package Naming Convention
```
com.[company].[project].[module]
Example: com.wtv.userservice.controller
```

#### File Naming Convention
- Entity class: `User.java`
- Controller: `UserController.java`
- Service interface: `UserService.java`
- Service implementation: `UserServiceImpl.java`
- DAO interface: `UserDao.java`
- DTO class: `UserDto.java`

#### Configuration File Convention
- Main configuration: `application.yml`
- Environment configuration: `application-{env}.yml`
- Logging configuration: `logback-spring.xml`

### 5. Project Type Specific Components

#### For API Projects
- **docs/api/**: API documentation
- **docs/examples/api-examples.md**: API usage examples
- **docs/examples/curl-examples.sh**: cURL command examples
- **OpenAPI**: API documentation generation

#### For Task-Based Projects
- **docs/tasks/**: Task-specific documentation
- **docs/operations/**: Operations and maintenance guides
- **docs/data/**: Data-related documentation
- **docs/examples/task-examples.md**: Task execution examples
- **docs/examples/config-examples/**: Configuration examples

#### Optional Components (All Projects)
- **Docker**: Containerized deployment
- **Kubernetes**: Container orchestration
- **GitHub Actions**: CI/CD
- **Maven Site**: Project site generation

### 6. Project Type Selection Guide

#### Choose Documentation Structure Based on Project Type

**API Projects**:
- Keep `docs/api/` directory
- Remove `docs/tasks/`, `docs/operations/`, `docs/data/` directories
- Focus on API documentation and client examples

**Task-Based Projects**:
- Keep `docs/tasks/`, `docs/operations/`, `docs/data/` directories
- Remove or minimize `docs/api/` directory
- Focus on task documentation and operational guides

**Hybrid Projects** (both API and tasks):
- Keep all documentation directories
- Clearly separate API and task functionalities in documentation

### 7. Important Notes

1. **Git Ignore**: Ensure `.gitignore` includes `target/`, `logs/`, `*.log`, etc.
2. **Environment Configuration**: Don't commit sensitive information to version control
3. **Documentation Maintenance**: Keep documentation synchronized with code updates
4. **Test Coverage**: Ensure critical business logic has test coverage
5. **Code Standards**: Follow team coding standards and best practices
6. **Project Type Consistency**: Choose appropriate documentation structure based on project type (API vs Task-based)
7. **Template Usage**: Use PROJECT-README-TEMPLATE.md for unified project documentation, and TASK-DOC-STANDARDS.md for task-specific documentation standards

---

**Template Version**: v1.0  
**Applicable Scope**: Java Projects  
**Last Updated**: 2025