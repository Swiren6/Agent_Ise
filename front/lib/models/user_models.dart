// lib/models/user_model.dart
class User {
  final String id;
  final String name;
  final String email;
  final String role;
  final String school;

  User({
    required this.id,
    required this.name,
    required this.email,
    required this.role,
    required this.school,
  });
}