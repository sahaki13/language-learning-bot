# Bot Học Ngoại Ngữ

Bot Telegram có sử dụng AI hỗ trợ để học Tiếng Việt, Tiếng Nga, và Tiếng Anh với chức năng sửa lỗi ngữ pháp.

---

## Bắt Đầu Nhanh (Cho Người Dùng)

### Thêm Bot vào Telegram
1. Mở Telegram
2. Tìm kiếm: **@LanguageLearningBot**
3. Nhấn "Start" hoặc gõ `/start`
4. Chọn ngôn ngữ (Tiếng Việt 🇻🇳 | Tiếng Nga 🇷🇺 | Tiếng Anh 🇬🇧)
5. Bắt đầu trò chuyện!

**Thế là xong! Không cần cài đặt gì cả.**

---

## Các Lệnh Có Sẵn

| Lệnh | Chức Năng |
|------|----------|
| `/start` | Bắt đầu bot & chọn ngôn ngữ |
| `/settings` | Đổi ngôn ngữ |
| `/mode` | Chọn chế độ học |
| `/stats` | Xem tiến bộ & thống kê |
| `/language` | Đổi ngôn ngữ muốn học |
| `/help` | Nhận sự giúp đỡ |

---

## Chế Độ Học Tập

Chọn cách bạn muốn học:

- **💬 Chỉ Chat** - Chỉ luyện tập nói chuyện bằng Tiếng Anh/Nga/Việt
- **💬✅ Chat + Sửa Lỗi** - Chat và nhận sửa lỗi ngữ pháp (Khuyên dùng!)
- **✅ Chỉ Sửa Lỗi** - Chỉ kiểm tra ngữ pháp, không chat

---

## Câu Hỏi Thường Gặp


**Dev:** Chưa ai dùng nên chưa ai hỏi ))

**Trong trường hợp nếu bạn có thắc mắc sau**

### Q: Nó có miễn phí không?
**A:** Có! Bot hoàn toàn miễn phí sử dụng.<sup>*</sup>

<sup>* Dev: hiện tại thì có, ~~sau này thì không~~ hẹ hẹ hẹ</sup>

### Q: Bot sai, tôi phải làm sao?
**A:** ~~Bot không sai, chỉ bạn sai~~ Vui lòng báo cáo thông qua biểu mẫu phản hồi của chúng tôi. Chúng tôi rất cảm ơn sự giúp đỡ!



---

## Thống Kê Học Tập Của Bạn

Sử dụng `/stats` để xem:
- 📝 Tổng số tin nhắn đã gửi
- ✅ Số lần sửa lỗi ngữ pháp
- 🌐 Các ngôn ngữ bạn đang học
- 🔥 Streak học tập (số ngày liên tiếp)
- 📅 Số ngày hoạt động

---

## Cách Gửi Phản Hồi

(Chúng) tôi luôn lắng nghe ý kiến của bạn để cải thiện sản phẩm của mình!

### Cách Chia Sẻ Ý Tưởng:

1. **📋 Biểu Mẫu Phản Hồi** - [sẽ cập nhật link sau](#)
   - Dùng cho: Yêu cầu tính năng, gợi ý, báo cáo lỗi
   - Mất: 2-3 phút
   - Có thể ẩn danh hoặc điền tên

2. **💬 Nhắn Tin Trực Tiếp**
   - Liên hệ trực tiếp qua các mạng xã hội, ứng dụng nhắn tin, email
   - Cho các câu hỏi hoặc vấn đề nhanh

---

## Lộ Trình Công Khai - Bình Chọn Tính Năng

Chúng tôi phát triển tính năng dựa trên **những gì BẠN muốn!**

### Cách Thức Hoạt Động:
1. Bạn gửi yêu cầu tính năng thông qua biểu mẫu
2. Chúng tôi thu thập tất cả yêu cầu và đếm votes
3. **Các tính năng được vote cao nhất sẽ xuất hiện ở đây** ⬇

### Sắp Tới:
Chúng tôi sẽ hiển thị các yêu cầu tính năng hàng đầu ở đây cùng số lượng vote và trạng thái triển khai!

**Muốn bình chọn?** Gửi ý tưởng của bạn thông qua biểu mẫu phản hồi (link ở trên).

---

## Hướng Dẫn Cài Đặt Cho Nhà Phát Triển (Khu Vực Chỉ Dành Cho Lập Trình Viên)

Nếu bạn muốn chạy bot trên máy tính cá nhân:

```bash
# 1. Clone repository
git clone https://github.com/sahaki13/language-learning-bot
cd language-learning-bot

# 2. Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Trên Windows: venv\Scripts\activate

# 3. Cài đặt dependencies
pip install -r requirements.txt

# 4. Tạo file .env với các key của bạn
echo "TELEGRAM_TOKEN=your_token_here" > .env
echo "GROQ_API_KEY=your_groq_key_here" >> .env
echo "DATABASE_URL=sqlite:///bot.db" >> .env

# 5. Chạy bot
python main.py
```

**Lấy keys của bạn:**
- 🤖 Telegram Token: Chat [@BotFather](https://t.me/botfather) → `/newbot`
- 🧠 Groq API Key: [console.groq.com](https://console.groq.com)

---

## Giấy Phép & Bản Quyền 📜

Copyright © 2026 sahaki13 (Language Learning Bot)

Dự án này được cấp phép theo **Giấy Phép MIT** - xem file [LICENSE](LICENSE) để biết chi tiết.

**Điều này có nghĩa gì?**
- ✅ Bạn có thể sử dụng bot này miễn phí
- ✅ Bạn có thể học từ code
- ✅ Bạn có thể sửa đổi cho mục đích cá nhân
- 📝 Vui lòng ghi công cho tác giả gốc nếu bạn chia sẻ/sửa đổi
- ❌ Bạn không thể tuyên bố nó là công trình của riêng bạn

---

## Đóng Góp 🤝

Hiện tại, chúng tôi không chấp nhận các đóng góp code. Tuy nhiên, chúng tôi **YÊU THÍCH** ý tưởng của bạn!

**Cách giúp đỡ:**
- Bình chọn cho tính năng thông qua biểu mẫu phản hồi
- Báo cáo lỗi
- Gợi ý cải tiến
- Chia sẻ bot với bạn bè!

---

## Hỗ Trợ

- 💬 **Telegram**: @hoangsatruongsalacuaVietNam
- 📋 **Biểu Mẫu Phản Hồi**: (Sắp Tới)
- 🐛 **Báo Cáo Lỗi**: Sử dụng biểu mẫu phản hồi với "Bug Report"

---

## Về Bot Này

Bot này được tạo ra để giúp những người học ngoại ngữ:
- Luyện tập nói chuyện một cách tự nhiên
- Nhận phản hồi sửa lỗi ngữ pháp tức thì
- Theo dõi tiến bộ theo thời gian
- Học tập theo tốc độ của riêng bạn

Được xây dựng với ~~sự miễn phí~~ sử dụng:
- 🤖 Telegram Bot API
- 🧠 Groq LLM (AI)
- 💾 PostgreSQL
- 🚀 Railway

---

**Chúc Bạn Học Tập Vui Vẻ!**

Nếu bạn thấy bot này hữu ích, vui lòng chia sẻ với bạn bè đang học ngôn ngữ!

---

# Language Learning Bot

AI-powered Telegram bot for learning Vietnamese, Russian, and English with grammar correction.

---

## Quick Start (For Users)

### Add Bot to Telegram
1. Open Telegram
2. Search for: **@LanguageLearningBot**
3. Click "Start" or type `/start`
4. Choose your language (Vietnamese 🇻🇳 | Russian 🇷🇺 | English 🇬🇧)
5. Start chatting!

**That's it! No installation needed.**

---

## Available Commands

| Command | What It Does |
|---------|-------------|
| `/start` | Start the bot & choose language |
| `/settings` | Change language |
| `/mode` | Choose learning mode |
| `/stats` | View your progress & stats |
| `/language` | Change the language you want to learn |
| `/help` | Get help |

---

## Learning Modes

Choose how you want to learn:

- **💬 Chat Only** - Just practice conversational English/Russian/Vietnamese
- **💬✅ Chat + Grammar** - Chat AND get grammar corrections (Recommended!)
- **✅ Grammar Only** - Only get grammar checking, no chat

---

## FAQ

---

## 📊 Your Learning Stats

Use `/stats` to see:
- 📝 Total messages sent
- ✅ Grammar corrections received
- 🌐 Languages you're practicing
- 🔥 Learning streak (consecutive days)
- 📅 Active days

---

## How to Send Feedback

We want to hear from you! Your ideas help us improve.

### Ways to Share Your Ideas:

1. **📋 Feedback Form** - [Coming Soon](#)
   - Best for: Feature requests, suggestions, bug reports
   - Takes: 2-3 minutes
   - Anonymous or with name

2. **💬 Direct Message**
   - Contact through social media, messaging apps, and email 
   - For quick questions or issues

---

## Public Roadmap - Feature Voting

We develop features based on **what YOU want!**

### How It Works:
1. You submit a feature request via the form
2. We collect all requests and count votes
3. **Top voted features appear here** ⬇

### Coming Soon:
We will display top feature requests here with vote counts and implementation status!

**Want to vote?** Submit your ideas via the feedback form (link above).

---

## Developer Setup (For Developers Only)

If you want to run the bot locally on your computer:

```bash
# 1. Clone repository
git clone https://github.com/sahaki13/language-learning-bot
cd language-learning-bot

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file with your keys
echo "TELEGRAM_TOKEN=your_token_here" > .env
echo "GROQ_API_KEY=your_groq_key_here" >> .env
echo "DATABASE_URL=sqlite:///bot.db" >> .env

# 5. Run the bot
python main.py
```

**Get your keys:**
- 🤖 Telegram Token: Chat [@BotFather](https://t.me/botfather) → `/newbot`
- 🧠 Groq API Key: [console.groq.com](https://console.groq.com)

---

## License & Copyright 📜

Copyright © 2026 sahaki13 (Language Learning Bot)

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

**What does this mean?**
- ✅ You can use this bot for free
- ✅ You can learn from the code
- ✅ You can modify it for personal use
- 📝 Please credit the original author if you share/modify it
- ❌ You cannot claim it as your own work

---

## Contributing 🤝

Currently, we're not accepting code contributions. However, we **LOVE** your ideas!

**How to help:**
- Vote for features via feedback form
- Report bugs
- Suggest improvements
- Share the bot with friends!

---

## Support

- 💬 **Telegram**: @hoangsatruongsalacuaVietNam
- 📋 **Feedback Form**: (Coming Soon)
- 🐛 **Report Bug**: Use feedback form with "Bug Report"

---

## 🎓 About This Bot

This bot was created to help language learners:
- Practice speaking naturally
- Get instant grammar feedback
- Track progress over time
- Learn at their own pace

Built using:
- 🤖 Telegram Bot API
- 🧠 Groq LLM (AI)
- 💾 PostgreSQL
- 🚀 Railway

---

**Happy Learning!**

If you find this bot helpful, please share it with friends who are learning languages too!