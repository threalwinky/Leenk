class Webhook:
    def __init__(self):
        self.log = {}
    def create_webhook(self, webhook_id):
        if webhook_id in self.log:
            return "Webhook ID already exists", 400
        self.log[webhook_id] = []
        return f"Webhook {webhook_id} created", 201
    def add_log(self, webhook_id, message):
        if webhook_id not in self.log:
            return "Webhook ID does not exist", 404
        self.log[webhook_id].append(message)
        return f"Log added to webhook {webhook_id}", 200
    def clear_logs(self):
        self.log.clear()
        return "All webhook logs cleared", 200