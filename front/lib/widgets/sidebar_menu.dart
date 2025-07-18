// import 'package:flutter/material.dart';
// import '../screens/chat_screen.dart'; // Assurez-vous d'importer votre ChatScreen

// class SidebarMenu extends StatelessWidget {
//   const SidebarMenu({super.key});

//   @override
//   Widget build(BuildContext context) {
//     return Drawer(
//       child: ListView(
//         padding: EdgeInsets.zero,
//         children: [
//           const DrawerHeader(
//             decoration: BoxDecoration(color: Colors.blue),
//             child: Column(
//               crossAxisAlignment: CrossAxisAlignment.start,
//               mainAxisAlignment: MainAxisAlignment.end,
//               children: [
//                 CircleAvatar(radius: 24, child: Icon(Icons.school, size: 30)),
//                 SizedBox(height: 8),
//                 Text(
//                   'Assistant Scolaire',
//                   style: TextStyle(
//                     color: Colors.white,
//                     fontSize: 18,
//                     fontWeight: FontWeight.bold,
//                   ),
//                 ),
//                 Text(
//                   'Édition Éducation',
//                   style: TextStyle(color: Colors.white70, fontSize: 14),
//                 ),
//               ],
//             ),
//           ),
//           ListTile(
//             leading: const Icon(Icons.chat),
//             title: const Text('Chat AI'),
//             onTap: () {
//               Navigator.pop(context); // Ferme le drawer
//               Navigator.push(
//                 context,
//                 MaterialPageRoute(builder: (context) => const ChatScreen()),
//               );
//             },
//           ),
//           ListTile(
//             leading: const Icon(Icons.library_books),
//             title: const Text('Historiques'),
//             onTap: () {
//               Navigator.pop(context);
//               // Navigation vers les historiques
//             },
//           ),
//           const Divider(),
//           ListTile(
//             leading: const Icon(Icons.person),
//             title: const Text('Profil'),
//             onTap: () {
//               Navigator.pop(context);
//               // Navigation vers le profil
//             },
//           ),
//           ListTile(
//             leading: const Icon(Icons.settings),
//             title: const Text('Paramètres'),
//             onTap: () {
//               Navigator.pop(context);
//               // Navigation vers les paramètres
//             },
//           ),
//           ListTile(
//             leading: const Icon(Icons.exit_to_app),
//             title: const Text('Déconnexion'),
//             onTap: () {
//               // Déconnexion
//               Navigator.popUntil(context, (route) => route.isFirst);
//             },
//           ),
//         ],
//       ),
//     );
//   }
// }


import 'package:flutter/material.dart';
import '../screens/chat_screen.dart';

class SidebarMenu extends StatelessWidget {
  const SidebarMenu({super.key});

  @override
  Widget build(BuildContext context) {
    return Drawer(
      child: Column(
        children: [
          DrawerHeader(
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                colors: [Colors.blueAccent, Colors.lightBlue],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
            ),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                const CircleAvatar(
                  radius: 30,
                  backgroundColor: Colors.white,
                  child: Icon(Icons.school, size: 30, color: Colors.blue),
                ),
                const SizedBox(width: 16),
                Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: const [
                    Text(
                      'Assistant Scolaire',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    Text(
                      'Édition Éducation',
                      style: TextStyle(
                        color: Colors.white70,
                        fontSize: 14,
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
          _buildMenuItem(
            icon: Icons.chat,
            label: 'Chat IA',
            onTap: () {
              Navigator.pop(context);
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const ChatScreen()),
              );
            },
          ),
          _buildMenuItem(
            icon: Icons.history,
            label: 'Historiques',
            onTap: () {
              Navigator.pop(context);
              // Ajouter navigation vers historique
            },
          ),
          const Divider(),
          _buildMenuItem(
            icon: Icons.person,
            label: 'Profil',
            onTap: () {
              Navigator.pop(context);
              // Ajouter navigation vers profil
            },
          ),
          _buildMenuItem(
            icon: Icons.settings,
            label: 'Paramètres',
            onTap: () {
              Navigator.pop(context);
              // Ajouter navigation vers paramètres
            },
          ),
          const Spacer(),
          _buildMenuItem(
            icon: Icons.exit_to_app,
            label: 'Déconnexion',
            onTap: () {
              Navigator.popUntil(context, (route) => route.isFirst);
            },
          ),
          const SizedBox(height: 16),
        ],
      ),
    );
  }

  Widget _buildMenuItem({
    required IconData icon,
    required String label,
    required VoidCallback onTap,
  }) {
    return ListTile(
      leading: Icon(icon, color: Colors.blueAccent),
      title: Text(label),
      onTap: onTap,
    );
  }
}