class PyDatabaseClient {
    // ... (previous methods) ...

    async executeQuery(query, params = null) {
        return this._makeRequest('POST', 'query', {
            query,
            params
        });
    }

    async createTable(tableName, columns) {
        return this._makeRequest('POST', 'table', {
            table_name: tableName,
            columns
        });
    }

    async getTableSchema(tableName) {
        return this._makeRequest('GET', `table/${tableName}/schema`);
    }

    // Helper methods for common SQL operations
    async selectAll(tableName, conditions = null) {
        let query = `SELECT * FROM ${tableName}`;
        if (conditions) {
            query += ` WHERE ${conditions}`;
        }
        return this.executeQuery(query);
    }

    async insertInto(tableName, data) {
        const columns = Object.keys(data);
        const values = Object.values(data);
        const placeholders = new Array(values.length).fill('?').join(', ');
        
        const query = `
            INSERT INTO ${tableName} 
            (${columns.join(', ')}) 
            VALUES (${placeholders})
        `;
        
        return this.executeQuery(query, values);
    }

    async updateTable(tableName, data, conditions) {
        const setClause = Object.keys(data)
            .map(key => `${key} = ?`)
            .join(', ');
        const values = [...Object.values(data)];
        
        let query = `UPDATE ${tableName} SET ${setClause}`;
        if (conditions) {
            query += ` WHERE ${conditions}`;
        }
        
        return this.executeQuery(query, values);
    }
}

// Usage example:
async function sqlExample() {
    const client = new PyDatabaseClient();
    
    try {
        await client.login('your-password');
        
        // Create a new table
        await client.createTable('employees', {
            name: 'TEXT',
            email: 'TEXT',
            salary: 'REAL'
        });
        
        // Insert data
        await client.insertInto('employees', {
            name: 'John Doe',
            email: 'john@example.com',
            salary: 75000.00
        });
        
        // Query data
        const result = await client.selectAll('employees', "salary > 50000");
        console.log('Employees:', result.rows);
        
        // Update data
        await client.updateTable(
            'employees',
            { salary: 80000.00 },
            "name = 'John Doe'"
        );
        
        // Get table schema
        const schema = await client.getTableSchema('employees');
        console.log('Table schema:', schema);
        
    } catch (error) {
        console.error('Error:', error);
    }
}