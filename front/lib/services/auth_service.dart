import 'package:flutter/foundation.dart';
import '../models/user_models.dart';

class AuthService with ChangeNotifier {
  User? _user;
  bool _isAuthenticated = false;

  User? get user => _user;
  bool get isAuthenticated => _isAuthenticated;

  Future<void> login(String email, String password) async {
    // Simulation d'authentification
    await Future.delayed(const Duration(seconds: 1));

    _user = User(
      id: '1',
      name: 'Élève Test',
      email: email,
      role: 'student',
      school: 'Lycée International',
    );
    _isAuthenticated = true;
    notifyListeners();
  }

  Future<void> logout() async {
    _user = null;
    _isAuthenticated = false;
    notifyListeners();
  }
}
