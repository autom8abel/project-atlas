-- Create the 'users' table to store anyone who interacts with the system.
-- This includes you (the admin) and, in the future, your agency's clients.
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,                   -- A unique, auto-incrementing ID for each user
    email VARCHAR(255) UNIQUE NOT NULL,      -- Ensures no two users can have the same email
    hashed_password VARCHAR(255) NOT NULL,   -- Stores the bcrypt-hashed password, never plain text
    full_name VARCHAR(255),                  -- The user's full name
    company_name VARCHAR(255),               -- Important for your agency niche
    is_active BOOLEAN DEFAULT TRUE,          -- Allows for soft-deletes (deactivating instead of deleting)
    is_superuser BOOLEAN DEFAULT FALSE,      -- Flags if the user has admin privileges
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP, -- Automatically records creation time
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP  -- Tracks the last update time
);

-- Create the 'tasks' table.
-- The core of a productivity assistant: managing to-do items.
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE, -- The owner of the task. CASCADE: if user is deleted, their tasks are too.
    title VARCHAR(255) NOT NULL,             -- A short description of the task
    description TEXT,                        -- More detailed notes
    due_date TIMESTAMPTZ,                    -- When the task is due (with timezone)
    category VARCHAR(100),                   -- Finance-focused: 'bookkeeping', 'tax', 'invoice', 'reporting'
    status VARCHAR(50) DEFAULT 'pending',    -- 'pending', 'in_progress', 'completed'
    is_important BOOLEAN DEFAULT FALSE,      -- A flag for priority tasks
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Create an index on the user_id column in the tasks table for faster query performance.
CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);

-- Create a function to automatically update the 'updated_at' column
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create a trigger to automatically update the 'updated_at' timestamp on users
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create a trigger to automatically update the 'updated_at' timestamp on tasks
CREATE TRIGGER update_tasks_updated_at BEFORE UPDATE ON tasks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
