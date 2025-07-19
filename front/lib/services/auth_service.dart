

import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

class AuthService with ChangeNotifier {
  String? _token;
  int? _userId;
  List<String>? _roles; 
  bool? _changepassword;

  bool get isAuthenticated => _token != null;
  int? get userId => _userId;
  List<String>? get roles => _roles;
  bool? get mustChangePassword => _changepassword;

  static const String _baseUrl = 'http://192.168.56.1:5000';

  List<String> _parseRoles(dynamic rolesData) {
    debugPrint('[AuthService] Raw roles type: ${rolesData.runtimeType}');
    debugPrint('[AuthService] Raw roles value: $rolesData');

    try {
      if (rolesData is List) {
        return rolesData.map((e) => e.toString()).toList();
      }
      
      if (rolesData is String) {
        final decoded = json.decode(rolesData);
        if (decoded is List) {
          return decoded.map((e) => e.toString()).toList();
        }
        return [decoded.toString()];
      }
      
      return [rolesData.toString()];
    } catch (e) {
      debugPrint('[AuthService] Error parsing roles: $e');
      return [];
    }
  }

  bool _parseChangePassword(dynamic value) {
    debugPrint('[AuthService] Raw changepassword type: ${value.runtimeType}');
    debugPrint('[AuthService] Raw changepassword value: $value');

    if (value is bool) return value;
    if (value is int) return value == 1;
    if (value is String) return value.toLowerCase() == 'true' || value == '1';
    return false;
  }

  Future<bool> login(String loginIdentifier, String password) async {
    final url = Uri.parse('$_baseUrl/api/login');

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
        
        _token = responseData['token']?.toString();
        _userId = int.tryParse(responseData['idpersonne']?.toString() ?? '');
        _roles = _parseRoles(responseData['roles']);
        _changepassword = _parseChangePassword(responseData['changepassword']);

        if (_token == null || _userId == null) {
          throw Exception('Invalid response data');
        }

        final prefs = await SharedPreferences.getInstance();
        await Future.wait([
          prefs.setString('auth_token', _token!),
          prefs.setInt('user_id', _userId!),
          prefs.setString('user_roles', json.encode(_roles)),
          prefs.setBool('changepassword', _changepassword ?? false),
        ]);

        notifyListeners();
        return true;
      } else {
        final error = json.decode(response.body);
        throw Exception(error['message'] ?? 'Login failed');
      }
    } catch (e) {
      debugPrint('[AuthService] Login error: $e');
      rethrow;
    }
  }

  Future<bool> autoLogin() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('auth_token');
      final userId = prefs.getInt('user_id');
      final rolesString = prefs.getString('user_roles');
      final changepassword = prefs.getBool('changepassword');

      if (token != null && userId != null) {
        _token = token;
        _userId = userId;
        _roles = rolesString != null 
            ? _parseRoles(json.decode(rolesString))
            : [];
        _changepassword = changepassword;
        notifyListeners();
        return true;
      }
      return false;
    } catch (e) {
      debugPrint('[AuthService] Auto login error: $e');
      return false;
    }
  }

  Future<void> logout() async {
    _token = null;
    _userId = null;
    _roles = null;
    _changepassword = null;
    notifyListeners();

    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.clear();
    } catch (e) {
      debugPrint('[AuthService] Logout error: $e');
    }
  }
}