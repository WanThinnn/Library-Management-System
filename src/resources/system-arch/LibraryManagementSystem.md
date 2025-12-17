graph TB
    subgraph "PRESENTATION LAYER"
        A[Web Browser]
    end

    subgraph "BUSINESS LAYER"
        B[Nginx]
        C[Gunicorn]
        D[Django Application]
    end

    subgraph "DATA LAYER"
        E[Django ORM]
        F[PostgreSQL Server]
        G[(Library Database)]
    end

    subgraph "STORAGE LAYER"
        H[Firebase Storage<br/>Static Files - CSS, JS, Images]
    end

    A -->|Request HTML| B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> F
    F --> E
    E --> D
    D -->|HTML Response| C
    C --> B
    B --> A
    
    A -->|Request Static Files<br/>CSS, JS, Images| H
    H -->|Return Static Files| A
    
    D -.->|Upload Static Files| H

    style A fill:#FFE6E6,stroke:#333,stroke-width:2px
    style D fill:#E6F3FF,stroke:#333,stroke-width:2px
    style G fill:#E6FFE6,stroke:#333,stroke-width:2px
    style H fill:#FFF3E6,stroke:#333,stroke-width:2px