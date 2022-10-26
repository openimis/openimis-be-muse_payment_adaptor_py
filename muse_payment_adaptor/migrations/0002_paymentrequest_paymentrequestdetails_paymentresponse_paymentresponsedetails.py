# Generated by Django 3.2.15 on 2022-10-26 13:01

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('muse_payment_adaptor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentRequest',
            fields=[
                ('id', models.UUIDField(db_column='Id',
                 default=uuid.uuid4, primary_key=True, serialize=False)),
                ('message_id', models.CharField(
                    db_column='MessageId', max_length=50)),
                ('payment_type', models.CharField(blank=True,
                 db_column='PaymentType', max_length=50, null=True)),
                ('reference_no', models.CharField(blank=True,
                 db_column='ReferenceNo', max_length=50, null=True)),
                ('payment_description', models.CharField(blank=True,
                 db_column='PaymentDescription', max_length=300, null=True)),
                ('total_amount', models.DecimalField(
                    blank=True, db_column='TotalAmount', decimal_places=4, max_digits=18, null=True)),
                ('no_of_tnx', models.IntegerField(
                    blank=True, db_column='NoOfTnx', null=True)),
                ('payment_date', models.DateField(
                    blank=True, db_column='PaymentDate', null=True)),
                ('status', models.CharField(blank=True,
                 db_column='Status', max_length=10, null=True)),
                ('record_date', models.DateTimeField(
                    auto_now=True, db_column='RecordDate')),
            ],
            options={
                'db_table': 'PaymentRequest',
            },
        ),
        migrations.CreateModel(
            name='PaymentResponse',
            fields=[
                ('id', models.UUIDField(db_column='Id',
                 default=uuid.uuid4, primary_key=True, serialize=False)),
                ('payment_request', models.ForeignKey(blank=True, db_column='PaymentRequestId', null=True,
                 on_delete=django.db.models.deletion.DO_NOTHING, to='muse_payment_adaptor.paymentrequest')),
                ('gateway_msg_id', models.CharField(blank=True,
                 db_column='GatewayMsgId', max_length=50, null=True)),
                ('message_type', models.CharField(blank=True,
                 db_column='MessageType', max_length=20, null=True)),
                ('payment_type', models.CharField(blank=True,
                 db_column='PaymentType', max_length=20, null=True)),
                ('response_date', models.DateTimeField(
                    blank=True, db_column='ResponseDate', null=True)),
                ('status', models.CharField(blank=True,
                 db_column='Status', max_length=20, null=True)),
                ('status_description', models.CharField(blank=True,
                 db_column='StatusDescription', max_length=200, null=True)),
                ('record_date', models.DateTimeField(
                    auto_now=True, db_column='RecordDate')),
            ],
            options={
                'db_table': 'PaymentResponse',
            },
        ),
        migrations.CreateModel(
            name='PaymentResponseDetails',
            fields=[
                ('id', models.UUIDField(db_column='Id',
                 default=uuid.uuid4, primary_key=True, serialize=False)),
                ('response', models.ForeignKey(blank=True, db_column='ResponseId', null=True,
                 on_delete=django.db.models.deletion.DO_NOTHING, to='muse_payment_adaptor.paymentresponse')),
                ('settlement_msg_id', models.CharField(blank=True,
                 db_column='SettlementMsgId', max_length=50, null=True)),
                ('payee_code', models.CharField(blank=True,
                 db_column='PayeeCode', max_length=10, null=True)),
                ('end_to_end', models.CharField(blank=True,
                 db_column='EndToEnd', max_length=50, null=True)),
                ('status', models.CharField(blank=True,
                 db_column='Status', max_length=20, null=True)),
                ('status_description', models.CharField(blank=True,
                 db_column='StatusDescription', max_length=200, null=True)),
                ('settlement_date', models.DateTimeField(
                    db_column='SettlementDate', null=True, blank=True)),
                ('record_date', models.DateTimeField(
                    auto_now=True, db_column='RecordDate')),
            ],
            options={
                'db_table': 'PaymentResponseDetails',
            },
        ),
        migrations.CreateModel(
            name='PaymentRequestDetails',
            fields=[
                ('id', models.UUIDField(db_column='Id',
                 default=uuid.uuid4, primary_key=True, serialize=False)),
                ('payment_request', models.ForeignKey(blank=True, db_column='PaymentRequestId', null=True,
                 on_delete=django.db.models.deletion.DO_NOTHING, to='muse_payment_adaptor.paymentrequest')),
                ('payee_code', models.CharField(blank=True,
                 db_column='PayeeCode', max_length=10, null=True)),
                ('name', models.CharField(blank=True,
                 db_column='Name', max_length=50, null=True)),
                ('acc_no', models.CharField(blank=True,
                 db_column='AccNo', max_length=20, null=True)),
                ('acc_name', models.CharField(blank=True,
                 db_column='AccName', max_length=100, null=True)),
                ('bank', models.CharField(blank=True,
                 db_column='Bank', max_length=50, null=True)),
                ('bank_bic', models.CharField(blank=True,
                 db_column='BankBIC', max_length=50, null=True)),
                ('amount', models.DecimalField(blank=True, db_column='Amount',
                 decimal_places=4, max_digits=18, null=True)),
                ('payment_channel', models.CharField(blank=True,
                 db_column='PaymentChannel', max_length=50, null=True)),
            ],
            options={
                'db_table': 'PaymentRequestDetails',
            },
        ),
    ]
