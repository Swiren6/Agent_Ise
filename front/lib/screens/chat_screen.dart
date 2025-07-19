import 'package:flutter/material.dart';
import '../widgets/custom_appbar.dart';
import '../widgets/message_bubble.dart';
import '../widgets/sidebar_menu.dart';
import '../models/message_models.dart';

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController _messageController = TextEditingController();
  final List<Message> _messages = [
    Message(text: 'Bonjour! Comment puis-je vous aider aujourd\'hui?', isMe: false),
  ];

  void _sendMessage() {
    if (_messageController.text.trim().isEmpty) return;

    setState(() {
      _messages.add(Message(text: _messageController.text, isMe: true));
      _messageController.clear();
    });

    // Simuler une réponse après un court délai
    Future.delayed(const Duration(seconds: 1), () {
      setState(() {
        _messages.add(
            Message(text: 'Je réfléchis à votre question...', isMe: false));
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CustomAppBar(
        title: 'Assistant Scolaire',
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              // Action pour rafraîchir la conversation
            },
          ),
        ],
      ),
      drawer: const SidebarMenu(),
      body: Column(
        children: [
          Expanded(
            child: Container(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [
                    Colors.blue.shade50,
                    Colors.white,
                  ],
                ),
              ),
              child: ListView.builder(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                reverse: false,
                itemCount: _messages.length,
                itemBuilder: (context, index) {
                  return MessageBubble(
                    message: _messages[index],
                    isMe: _messages[index].isMe,
                  );
                },
              ),
            ),
          ),
          _buildMessageInput(),
        ],
      ),
    );
  }

  Widget _buildMessageInput() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: [
          BoxShadow(
            color: Colors.grey.withOpacity(0.2),
            blurRadius: 8,
            offset: const Offset(0, -4),
          ),
        ],
      ),
      child: Row(
        children: [
          Expanded(
            child: TextField(
              controller: _messageController,
              decoration: InputDecoration(
                hintText: 'Tapez votre message...',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(24),
                  borderSide: BorderSide.none,
                ),
                filled: true,
                fillColor: Colors.grey.shade100,
                contentPadding: const EdgeInsets.symmetric(
                  horizontal: 16,
                  vertical: 12,
                ),
              ),
              textCapitalization: TextCapitalization.sentences,
              onSubmitted: (_) => _sendMessage(),
            ),
          ),
          const SizedBox(width: 8),
          Container(
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              gradient: LinearGradient(
                colors: [Colors.blueAccent, Colors.lightBlue.shade400],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
            ),
            child: IconButton(
              icon: const Icon(Icons.send, color: Colors.white),
              onPressed: _sendMessage,
            ),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _messageController.dispose();
    super.dispose();
  }
}


// import 'dart:convert';
// import 'package:flutter/material.dart';
// import '../models/message_models.dart';
// import '../services/api_service.dart'; // Vous allez créer ce service

// class ChatScreen extends StatefulWidget {
//   const ChatScreen({super.key});

//   @override
//   State<ChatScreen> createState() => _ChatScreenState();
// }

// class _ChatScreenState extends State<ChatScreen> {
//   final TextEditingController _messageController = TextEditingController();
//   final List<Message> _messages = [
//     Message(
//       text: 'Bonjour! Comment puis-je vous aider aujourd\'hui?', 
//       isMe: false,
//       isTyping: false,
//     ),
//   ];
//   bool _isLoading = false;

//   Future<void> _sendMessage() async {
//     if (_messageController.text.trim().isEmpty) return;

//     setState(() {
//       _messages.add(Message(
//         text: _messageController.text,
//         isMe: true,
//         isTyping: false,
//       ));
//       _messages.add(Message(
//         text: '',
//         isMe: false,
//         isTyping: true,
//       ));
//       _isLoading = true;
//       _messageController.clear();
//     });

//     try {
//       final response = await ApiService().askQuestion(_messages[_messages.length-2].text);
      
//       setState(() {
//         _messages.removeLast();
//         _messages.add(Message(
//           text: response,
//           isMe: false,
//           isTyping: false,
//         ));
//         _isLoading = false;
//       });
//     } catch (e) {
//       setState(() {
//         _messages.removeLast();
//         _messages.add(Message(
//           text: 'Désolé, une erreur est survenue: ${e.toString()}',
//           isMe: false,
//           isTyping: false,
//         ));
//         _isLoading = false;
//       });
//     }
//   }

//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       body: Column(
//         children: [
//           Expanded(
//             child: ListView.builder(
//               padding: const EdgeInsets.all(16),
//               itemCount: _messages.length,
//               itemBuilder: (context, index) {
//                 final message = _messages[index];
//                 return MessageBubble(
//                   message: message,
//                   isMe: message.isMe,
//                 );
//               },
//             ),
//           ),
//           if (_isLoading) const LinearProgressIndicator(),
//           _buildMessageInput(),
//         ],
//       ),
//     );
//   }

//   Widget _buildMessageInput() {
//     return Container(
//       padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
//       child: Row(
//         children: [
//           Expanded(
//             child: TextField(
//               controller: _messageController,
//               decoration: InputDecoration(
//                 hintText: 'Tapez votre question...',
//                 border: OutlineInputBorder(
//                   borderRadius: BorderRadius.circular(24),
//                 ),
//               ),
//               onSubmitted: (_) => _sendMessage(),
//             ),
//           ),
//           IconButton(
//             icon: const Icon(Icons.send),
//             onPressed: _isLoading ? null : _sendMessage,
//           ),
//         ],
//       ),
//     );
//   }
// }