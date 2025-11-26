-- Initialize GJH Blog database
-- This file is automatically run when the PostgreSQL container starts

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant necessary permissions
GRANT ALL PRIVILEGES ON DATABASE gjh_blog TO gjh_admin;
