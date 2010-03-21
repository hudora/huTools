## Django Models

Django Models always should come with `created_at` and `updated_at` fields. They also should use a Field
called `designator` as ther primary means of reference. If the designator is meant for human consumption it
should consist of a two letter Prefix unique for that model, a secquence number and a check digit. If the
designator is not (or seldom) for human consumption it should be a random unique value frefixed by two
letters. See  https://cybernetics.hudora.biz/intern/trac/wiki/NummernKreise prefixes used so far.


    class Task(models.Model):
        id = models.AutoField(primary_key=True)
        designator = models.CharField(max_length=32, default='', blank=True, editable=False, db_index=True,
            unique=True)
        created_at = models.DateField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
    
    def _task_post_save_cb(signal, sender, instance, **kwargs):
        if not instance.designator:
            chash = hashlib.md5("%f-%f-%d" % (random.random(), time.time(), instance.id))
            instance.designator = "TC%s" % base64.b32encode(chash.digest()).rstrip('=')
            # instance.designator = huTools.checksumming.build_verhoeff_id("TC", instance.id)
            instance.save()
    models.signals.post_save.connect(_task_post_save_cb, Task)
