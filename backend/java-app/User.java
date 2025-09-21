import java.sql.*;

public class User {
    private int id;
    private String username;
    private String email;
    private String password;

    public User(String username, String email, String password) {
        this.username = username;
        this.email = email;
        this.password = password;
    }

    private Connection connect() throws SQLException {
        try {
            Class.forName("org.sqlite.JDBC");
            return DriverManager.getConnection("jdbc:sqlite:jobs.db");
        } catch (Exception e) {
            throw new SQLException(e);
        }
    }

    public boolean register() {
        try (Connection conn = connect()) {
            PreparedStatement stmt = conn.prepareStatement(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)");
            stmt.setString(1, username);
            stmt.setString(2, email);
            stmt.setString(3, password);
            stmt.executeUpdate();
            return true;
        } catch (SQLException e) {
            System.out.println("⚠ Registration failed: " + e.getMessage());
            return false;
        }
    }

    public boolean login() {
        try (Connection conn = connect()) {
            PreparedStatement stmt = conn.prepareStatement(
                "SELECT * FROM users WHERE username=? AND password=?");
            stmt.setString(1, username);
            stmt.setString(2, password);
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                this.id = rs.getInt("id");
                this.email = rs.getString("email");
                return true;
            }
            return false;
        } catch (SQLException e) {
            System.out.println("⚠ Login failed: " + e.getMessage());
            return false;
        }
    }

    public int getId() {
        return id;
    }

    @Override
    public String toString() {
        return "User{username='" + username + "', email='" + email + "'}";
    }
}
