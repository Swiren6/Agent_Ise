import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

class AuthService with ChangeNotifier {
  String? _token;
  int? _userId;
  String? _username;

  bool get isAuthenticated => _token != null;
  int? get userId => _userId;
  String? get username => _username;

  static const String _baseUrl = 'http://localhost:5000'; 

  Future<bool> login(String loginIdentifier, String password) async {
  final url = Uri.parse('http://10.0.2.2:5000/api/login'); // Android
  // final url = Uri.parse('http://localhost:5000/api/login'); // iOS

  try {
    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'login_identifier': loginIdentifier,
        'password': password,
      }),
    );

    if (response.statusCode == 200) {
      final responseData = json.decode(response.body);
      _token = responseData['token'];
      _userId = responseData['idpersonne']; // Corrigé pour correspondre à votre API
      _username = responseData.get('username') ?? '';
      
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('auth_token', _token!);
      await prefs.setInt('user_id', _userId!);
      notifyListeners();
      return true;
    }
    return false;
  } catch (e) {
    debugPrint('Login error: $e');
    return false;
  }
}
  Future<bool> autoLogin() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('auth_token');
      final userId = prefs.getInt('user_id');
      final username = prefs.getString('username');
      
      if (token != null && userId != null && username != null) {
        _token = token;
        _userId = userId;
        _username = username;
        notifyListeners();
        return true;
      }
      return false;
    } catch (e) {
      if (kDebugMode) print('Auto login error: $e');
      return false;
    }
  }

  Future<void> logout() async {
    try {
      _token = null;
      _userId = null;
      _username = null;
      
      final prefs = await SharedPreferences.getInstance();
      await prefs.remove('auth_token');
      await prefs.remove('user_id');
      await prefs.remove('username');
      notifyListeners();
    } catch (e) {
      if (kDebugMode) print('Logout error: $e');
    }
  }
}