import java.sql.*;

public class HelpRequest {
    private String title;
    private String description;

    public HelpRequest(String title, String description) {
        this.title = title;
        this.description = description;
    }

    // Save request to DB
    public boolean save(int userId) {
        try (Connection conn = DriverManager.getConnection("jdbc:sqlite:jobs.db")) {
            PreparedStatement stmt = conn.prepareStatement(
                "INSERT INTO help_requests (title, description, user_id) VALUES (?, ?, ?)");
            stmt.setString(1, title);
            stmt.setString(2, description);
            stmt.setInt(3, userId);
            stmt.executeUpdate();
            return true;
        } catch (SQLException e) {
            System.out.println("⚠ Failed to save request: " + e.getMessage());
            return false;
        }
    }

    @Override
    public String toString() {
        return "HelpRequest{title='" + title + "', description='" + description + "'}";
    }
}
