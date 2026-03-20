from rest_framework import serializers
from .models import FarmTask, Field, Livestock, Transaction

class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = '__all__'

class LivestockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livestock
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class FarmTaskSerializer(serializers.ModelSerializer):
    field_name = serializers.ReadOnlyField(source='related_field.name')
    livestock_tag = serializers.ReadOnlyField(source='related_livestock.tag_id')

    class Meta:
        model = FarmTask
        fields = '__all__'

    def to_internal_value(self, data):
        """
        Bulletproof data cleaner. Converts names to IDs safely.
        """
        # Safely convert to a standard dictionary we can modify
        if hasattr(data, 'dict'):
            resource_data = data.dict()
        else:
            resource_data = dict(data)
        
        # 1. Convert empty strings to None/null
        nullable_fields = ['due_date', 'related_field', 'related_livestock']
        for field in nullable_fields:
            if resource_data.get(field) == "":
                resource_data[field] = None
                
        # 2. BULLETPROOF TRANSLATOR: Field Name -> Field ID
        rf_value = resource_data.get('related_field')
        if rf_value and isinstance(rf_value, str) and not rf_value.isdigit():
            # .strip() removes accidental spaces, __iexact ignores capitalization
            field_obj = Field.objects.filter(name__iexact=rf_value.strip()).first()
            if field_obj:
                resource_data['related_field'] = field_obj.id
            else:
                # If we STILL can't find it, force it to None to prevent the 400 crash
                resource_data['related_field'] = None
                
        # 3. BULLETPROOF TRANSLATOR: Livestock Tag -> Livestock ID
        rl_value = resource_data.get('related_livestock')
        if rl_value and isinstance(rl_value, str) and not rl_value.isdigit():
            livestock_obj = Livestock.objects.filter(tag_id__iexact=rl_value.strip()).first()
            if livestock_obj:
                resource_data['related_livestock'] = livestock_obj.id
            else:
                resource_data['related_livestock'] = None

        return super().to_internal_value(resource_data)