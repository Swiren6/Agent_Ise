import 'package:flutter/material.dart';
import '../models/message_models.dart';

class MessageBubble extends StatelessWidget {
  final Message message;
  final bool isMe;

  const MessageBubble({super.key, required this.message, required this.isMe});

  @override
  Widget build(BuildContext context) {
    final bubbleColor = isMe ? Colors.lightBlueAccent : Colors.grey.shade200;
    final textColor = isMe ? Colors.white : Colors.black87;
    final alignment = isMe ? MainAxisAlignment.end : MainAxisAlignment.start;
    final borderRadius = isMe
        ? const BorderRadius.only(
            topLeft: Radius.circular(16),
            topRight: Radius.circular(16),
            bottomLeft: Radius.circular(16),
          )
        : const BorderRadius.only(
            topLeft: Radius.circular(16),
            topRight: Radius.circular(16),
            bottomRight: Radius.circular(16),
          );

    return Row(
      mainAxisAlignment: alignment,
      crossAxisAlignment: CrossAxisAlignment.end,
      children: [
        if (!isMe) ...[
          const CircleAvatar(
            radius: 16,
            backgroundColor: Colors.deepPurple,
            child: Icon(Icons.smart_toy, size: 16, color: Colors.white),
          ),
          const SizedBox(width: 6),
        ],
        Flexible(
          child: Container(
            margin: const EdgeInsets.symmetric(vertical: 4),
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            decoration: BoxDecoration(
              color: bubbleColor,
              borderRadius: borderRadius,
            ),
            child: Text(
              message.text,
              style: TextStyle(color: textColor, fontSize: 16),
            ),
          ),
        ),
        if (isMe) const SizedBox(width: 6),
      ],
    );
  }
}


// class MessageBubble extends StatelessWidget {
//   final Message message;
//   final bool isMe;

//   const MessageBubble({
//     super.key,
//     required this.message,
//     required this.isMe,
//   });

//   @override
//   Widget build(BuildContext context) {
//     return Align(
//       alignment: isMe ? Alignment.centerRight : Alignment.centerLeft,
//       child: Container(
//         margin: const EdgeInsets.symmetric(vertical: 4, horizontal: 8),
//         padding: const EdgeInsets.all(12),
//         decoration: BoxDecoration(
//           color: isMe ? Colors.blue[100] : Colors.grey[200],
//           borderRadius: BorderRadius.circular(12),
//         ),
//         child: message.isTyping
//             ? const TypingIndicator()
//             : Text(message.text),
//       ),
//     );
//   }
// }

// class TypingIndicator extends StatelessWidget {
//   const TypingIndicator({super.key});

//   @override
//   Widget build(BuildContext context) {
//     return const Row(
//       mainAxisSize: MainAxisSize.min,
//       children: [
//         Text('Assistant tape...'),
//         SizedBox(width: 8),
//         SizedBox(
//           width: 20,
//           height: 20,
//           child: CircularProgressIndicator(strokeWidth: 2),
//         ),
//       ],
//     );
//   }
// }