from django import forms
from .models import AircraftModel, MasterComponentAssembly
from django.core.exceptions import ValidationError


class AircraftModelForm(forms.ModelForm):
    class Meta:
        model = AircraftModel
        fields = '__all__'

    def clean(self):
        """
        Checks that all the words belong to the sentence's language.
        """
        master_components = self.cleaned_data.get('master_components')
        components_that_have_assembly = []
        assemblies_are_ok = True
        for master_component in master_components:
            if master_component.assembly: 
                components_that_have_assembly.append(master_component)
        relevant_assemblies = []
        if components_that_have_assembly:
            # all the assemblies that have this component
            r_a = MasterComponentAssembly.objects.filter(assembly_components__in = components_that_have_assembly).distinct()
            for r in r_a:
                relevant_assemblies.append(r)
            
            for sub_assembly in relevant_assemblies:
                assembly_components = sub_assembly.assembly_components

                for assembly_component in assembly_components.all():

                    if assembly_component not in master_components:
                        assemblies_are_ok = False
           
                        break

    
        if not assemblies_are_ok:
            raise ValidationError("You have components selected that are part of an assembly, however that assembly is incomplete")
        return self.cleaned_data