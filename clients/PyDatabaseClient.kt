class PyDatabaseClient(
    // ... (previous properties) ...
) {
    // ... (previous methods) ...

    suspend fun executeQuery(query: String, params: List<Any>? = null): JSONObject {
        val body = JSONObject()
            .put("query", query)
            .put("params", JSONArray(params ?: emptyList<Any>()))
        return makeRequest("POST", "query", body)
    }

    suspend fun createTable(tableName: String, columns: Map<String, String>): JSONObject {
        val body = JSONObject()
            .put("table_name", tableName)
            .put("columns", JSONObject(columns))
        return makeRequest("POST", "table", body)
    }

    suspend fun getTableSchema(tableName: String): JSONObject {
        return makeRequest("GET", "table/$tableName/schema")
    }

    // Helper methods for common SQL operations
    suspend fun selectAll(tableName: String, conditions: String? = null): List<JSONObject> {
        val query = buildString {
            append("SELECT * FROM $tableName")
            if (conditions != null) {
                append(" WHERE $conditions")
            }
        }
        
        val response = executeQuery(query)
        return response.getJSONArray("rows").run {
            List(length()) { i -> getJSONObject(i) }
        }
    }

    suspend fun insertInto(tableName: String, data: JSONObject): JSONObject {
        val columns = data.keys().asSequence().toList()
        val values = columns.map { data.get(it) }
        val placeholders = List(values.size) { "?" }.joinToString(", ")
        
        val query = """
            INSERT INTO $tableName 
            (${columns.joinToString(", ")}) 
            VALUES ($placeholders)
        """.trimIndent()
        
        return executeQuery(query, values)
    }

    suspend fun updateTable(
        tableName: String,
        data: JSONObject,
        conditions: String? = null
    ): JSONObject {
        val setClause = data.keys().asSequence()
            .map { "$it = ?" }
            .joinToString(", ")
        val values = data.keys().asSequence()
            .map { data.get(it) }
            .toList()
        
        val query = buildString {
            append("UPDATE $tableName SET $setClause")
            if (conditions != null) {
                append(" WHERE $conditions")
            }
        }
        
        return executeQuery(query, values)
    }
}

// Usage example:
suspend fun sqlExample() {
    val client = PyDatabaseClient()
    
    try {
        client.login("your-password")
        
        // Create a new table
        val columns = mapOf(
            "name" to "TEXT",
            "email" to "TEXT",
            "salary" to "REAL"
        )
        client.createTable("employees", columns)
        
        // Insert data
        val employeeData = JSONObject()
            .put("name", "John Doe")
            .put("email", "john@example.com")
            .put("salary", 75000.00)
        client.insertInto("employees", employeeData)
        
        // Query data
        val employees = client.selectAll("employees", "salary > 50000")
        println("Employees: $employees")
        
        // Update data
        val updateData = JSONObject().put("salary", 80000.00)
        client.updateTable("employees", updateData, "name = 'John Doe'")
        
        // Get table schema
        val schema = client.getTableSchema("employees")
        println("Table schema: $schema")
        
    } catch (e: Exception) {
        println("Error: ${e.message}")
    }
}