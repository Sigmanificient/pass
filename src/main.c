#include <unistd.h>
#include <stdlib.h>

#define SQLITE_HAS_CODEC 1

#include <sqlcipher/sqlite3.h>
#include <stdio.h>


int main(int argc, char** argv) {
    // Open a database connection
    sqlite3* db;
    int rc = sqlite3_open("db.sqlite", &db);
    if (rc) {
        fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return 1;
    }

    // Set the password for the database
    rc = sqlite3_key(db, "password", 8);
    if (rc) {
        fprintf(stderr, "Error setting password: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return 1;
    }

    // Create a table
    char* sql = "CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, name TEXT);";
    char* err_msg = 0;

    rc = sqlite3_exec(db, sql, 0, 0, &err_msg);
    if (rc != SQLITE_OK ) {
        fprintf(stderr, "SQL error: %s", err_msg);
        sqlite3_free(err_msg);
    }

    // Insert a row
    sql = "INSERT INTO test (name) VALUES ('OwO, UwU');";
    rc = sqlite3_exec(db, sql, 0, 0, &err_msg);
    if (rc != SQLITE_OK ) {
        fprintf(stderr, "SQL error: %s", err_msg);
        sqlite3_free(err_msg);
    }
    sqlite3_close(db);
    fprintf(stdout, "Done.\n");
    return 0;
}

