import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:flutter/foundation.dart'; 

import '../services/auth_service.dart';
import '../screens/chat_screen.dart';

class Auth {
  static Future<void> login(String loginIdentifier, String password, BuildContext context) async {
    try {
      final authService = Provider.of<AuthService>(context, listen: false);

      final success = await authService.login(loginIdentifier, password);
      if (!success) {
        _showErrorSnackbar(context, "Identifiant ou mot de passe incorrect");
      }
    } catch (e) {
      _showErrorSnackbar(context, "Erreur de connexion: ${e.toString()}");
    }
  }

  static Future<void> logout(BuildContext context) async {
    try {
      final authService = Provider.of<AuthService>(context, listen: false);
      await authService.logout();
    } catch (e) {
      if (kDebugMode) print('Logout error: $e');
    }
  }

  static void _showErrorSnackbar(BuildContext context, String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: Colors.red,
        duration: const Duration(seconds: 3),
      ),
    );
  }
}