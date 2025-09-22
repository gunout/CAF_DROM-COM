import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class CAF_DROMCOMAnalyzer:
    def __init__(self, territoire_name):
        self.territoire = territoire_name
        self.colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#F9A602', '#6A0572', 
                      '#AB83A1', '#5CAB7D', '#2A9D8F', '#E76F51', '#264653']
        
        self.start_year = 2002
        self.end_year = 2025
        
        # Configuration spécifique à chaque territoire DROM-COM
        self.config = self._get_territoire_config()
        
    def _get_territoire_config(self):
        """Retourne la configuration spécifique pour chaque CAF DROM-COM"""
        configs = {
            "Guadeloupe": {
                "allocataires_base": 120000,
                "budget_base": 450,
                "specificites": ["familles_nombreuses", "precarite", "vieillesse"]
            },
            "Martinique": {
                "allocataires_base": 110000,
                "budget_base": 420,
                "specificites": ["vieillesse", "dependance", "handicap"]
            },
            "Guyane": {
                "allocataires_base": 85000,
                "budget_base": 380,
                "specificites": ["jeunesse", "familles_nombreuses", "precarite"]
            },
            "La Réunion": {
                "allocataires_base": 220000,
                "budget_base": 680,
                "specificites": ["precarite", "emploi", "familles_monoparentales"]
            },
            "Mayotte": {
                "allocataires_base": 65000,
                "budget_base": 280,
                "specificites": ["jeunesse", "familles_nombreuses", "precarite_elevee"]
            },
            "Saint-Martin": {
                "allocataires_base": 18000,
                "budget_base": 85,
                "specificites": ["tourisme", "petite_enfance", "precarite"]
            },
            "Saint-Barthélemy": {
                "allocataires_base": 5000,
                "budget_base": 45,
                "specificites": ["vieillesse", "tourisme", "revenus_eleves"]
            },
            "Saint-Pierre-et-Miquelon": {
                "allocataires_base": 3500,
                "budget_base": 35,
                "specificites": ["isolement", "vieillesse", "petite_enfance"]
            },
            "Wallis-et-Futuna": {
                "allocataires_base": 8000,
                "budget_base": 55,
                "specificites": ["traditions", "jeunesse", "isolement"]
            },
            "Polynésie française": {
                "allocataires_base": 95000,
                "budget_base": 320,
                "specificites": ["isolement", "tourisme", "jeunesse"]
            },
            "Nouvelle-Calédonie": {
                "allocataires_base": 105000,
                "budget_base": 380,
                "specificites": ["nickel", "vieillesse", "precarite"]
            },
            # Configuration par défaut pour les autres territoires
            "default": {
                "allocataires_base": 50000,
                "budget_base": 200,
                "specificites": ["prestations_familiales", "logement", "solidarite"]
            }
        }
        
        return configs.get(self.territoire, configs["default"])
    
    def generate_financial_data(self):
        """Génère des données financières pour la CAF"""
        print(f"🏛️ Génération des données financières pour CAF {self.territoire}...")
        
        # Créer une base de données annuelle
        dates = pd.date_range(start=f'{self.start_year}-01-01', 
                             end=f'{self.end_year}-12-31', freq='Y')
        
        data = {'Annee': [date.year for date in dates]}
        
        # Données démographiques
        data['Nombre_Allocataires'] = self._simulate_allocataires(dates)
        data['Prestations_Versees'] = self._simulate_prestations(dates)
        
        # Recettes de la CAF
        data['Recettes_Totales'] = self._simulate_total_revenue(dates)
        data['Cotisations_Sociales'] = self._simulate_social_contributions(dates)
        data['Contributions_Etat'] = self._simulate_state_contributions(dates)
        data['Autres_Recettes'] = self._simulate_other_revenue(dates)
        
        # Dépenses de la CAF
        data['Depenses_Totales'] = self._simulate_total_expenses(dates)
        data['Prestations_Familiales'] = self._simulate_family_benefits(dates)
        data['Prestations_Logement'] = self._simulate_housing_benefits(dates)
        data['Prestations_Solidarite'] = self._simulate_solidarity_benefits(dates)
        data['Frais_Gestion'] = self._simulate_management_costs(dates)
        
        # Indicateurs financiers
        data['Taux_Couverture'] = self._simulate_coverage_rate(dates)
        data['Ratio_Gestion'] = self._simulate_management_ratio(dates)
        data['Solde_Compte'] = self._simulate_account_balance(dates)
        
        # Prestations spécifiques adaptées aux DROM-COM
        data['Allocations_Familiales'] = self._simulate_family_allocations(dates)
        data['ARS'] = self._simulate_ars(dates)
        data['APL'] = self._simulate_apl(dates)
        data['RSA'] = self._simulate_rsa(dates)
        data['Prime_Naissance'] = self._simulate_birth_grant(dates)
        
        df = pd.DataFrame(data)
        
        # Ajouter des tendances spécifiques aux CAF DROM-COM
        self._add_caf_trends(df)
        
        return df
    
    def _simulate_allocataires(self, dates):
        """Simule le nombre d'allocataires"""
        base_allocataires = self.config["allocataires_base"]
        
        allocataires = []
        for i, date in enumerate(dates):
            # Croissance démographique spécifique aux DROM-COM
            if self.territoire in ["Mayotte", "Guyane"]:
                growth_rate = 0.025  # Croissance très forte
            elif self.territoire in ["La Réunion", "Polynésie française"]:
                growth_rate = 0.018  # Croissance forte
            else:
                growth_rate = 0.012  # Croissance modérée
            
            growth = 1 + growth_rate * i
            allocataires.append(base_allocataires * growth)
        
        return allocataires
    
    def _simulate_prestations(self, dates):
        """Simule le montant total des prestations versées"""
        base_prestations = self.config["budget_base"] * 0.85  # 85% du budget en prestations
        
        prestations = []
        for i, date in enumerate(dates):
            if self.territoire in ["Mayotte", "Guyane"]:
                growth = 1 + 0.028 * i  # Croissance très forte
            elif self.territoire in ["La Réunion", "Polynésie française"]:
                growth = 1 + 0.022 * i  # Croissance forte
            else:
                growth = 1 + 0.018 * i  # Croissance modérée
                
            noise = np.random.normal(1, 0.07)
            prestations.append(base_prestations * growth * noise)
        
        return prestations
    
    def _simulate_total_revenue(self, dates):
        """Simule les recettes totales de la CAF"""
        base_revenue = self.config["budget_base"]
        
        revenue = []
        for i, date in enumerate(dates):
            if self.territoire in ["Mayotte", "Guyane"]:
                growth_rate = 0.042  # Croissance très forte
            elif self.territoire in ["La Réunion", "Polynésie française"]:
                growth_rate = 0.035  # Croissance forte
            else:
                growth_rate = 0.028  # Croissance modérée
                
            growth = 1 + growth_rate * i
            noise = np.random.normal(1, 0.08)
            revenue.append(base_revenue * growth * noise)
        
        return revenue
    
    def _simulate_social_contributions(self, dates):
        """Simule les cotisations sociales"""
        base_contributions = self.config["budget_base"] * 0.65
        
        contributions = []
        for i, date in enumerate(dates):
            if self.territoire in ["Mayotte", "Guyane"]:
                growth = 1 + 0.035 * i  # Croissance très forte
            elif self.territoire in ["La Réunion", "Polynésie française"]:
                growth = 1 + 0.028 * i  # Croissance forte
            else:
                growth = 1 + 0.022 * i  # Croissance modérée
                
            noise = np.random.normal(1, 0.06)
            contributions.append(base_contributions * growth * noise)
        
        return contributions
    
    def _simulate_state_contributions(self, dates):
        """Simule les contributions de l'État (plus importantes en DROM-COM)"""
        base_state = self.config["budget_base"] * 0.30  # Part plus importante
        
        state_contributions = []
        for i, date in enumerate(dates):
            year = date.year
            # Augmentation plus forte des contributions pour les DROM-COM
            if year >= 2010:
                if self.territoire in ["Mayotte", "Guyane"]:
                    increase = 1 + 0.022 * (year - 2010)  # Très forte augmentation
                elif self.territoire in ["La Réunion", "Polynésie française"]:
                    increase = 1 + 0.018 * (year - 2010)  # Forte augmentation
                else:
                    increase = 1 + 0.015 * (year - 2010)  # Augmentation modérée
            else:
                increase = 1
            
            noise = np.random.normal(1, 0.05)
            state_contributions.append(base_state * increase * noise)
        
        return state_contributions
    
    def _simulate_other_revenue(self, dates):
        """Simule les autres recettes"""
        base_other = self.config["budget_base"] * 0.05
        
        other_revenue = []
        for i, date in enumerate(dates):
            growth = 1 + 0.025 * i
            noise = np.random.normal(1, 0.10)
            other_revenue.append(base_other * growth * noise)
        
        return other_revenue
    
    def _simulate_total_expenses(self, dates):
        """Simule les dépenses totales"""
        base_expenses = self.config["budget_base"] * 0.95
        
        expenses = []
        for i, date in enumerate(dates):
            if self.territoire in ["Mayotte", "Guyane"]:
                growth = 1 + 0.038 * i  # Croissance très forte
            elif self.territoire in ["La Réunion", "Polynésie française"]:
                growth = 1 + 0.032 * i  # Croissance forte
            else:
                growth = 1 + 0.026 * i  # Croissance modérée
                
            noise = np.random.normal(1, 0.07)
            expenses.append(base_expenses * growth * noise)
        
        return expenses
    
    def _simulate_family_benefits(self, dates):
        """Simule les prestations familiales"""
        base_family = self.config["budget_base"] * 0.45
        
        # Ajustement selon les spécificités
        multiplier = 1.4 if "familles_nombreuses" in self.config["specificites"] else 1.0
        
        family_benefits = []
        for i, date in enumerate(dates):
            if self.territoire in ["Mayotte", "Guyane"]:
                growth = 1 + 0.032 * i  # Croissance très forte
            elif self.territoire in ["La Réunion", "Polynésie française"]:
                growth = 1 + 0.028 * i  # Croissance forte
            else:
                growth = 1 + 0.022 * i  # Croissance modérée
                
            noise = np.random.normal(1, 0.06)
            family_benefits.append(base_family * growth * multiplier * noise)
        
        return family_benefits
    
    def _simulate_housing_benefits(self, dates):
        """Simule les prestations logement"""
        base_housing = self.config["budget_base"] * 0.25
        
        housing_benefits = []
        for i, date in enumerate(dates):
            if self.territoire in ["Mayotte", "Guyane"]:
                growth = 1 + 0.035 * i  # Croissance très forte
            elif self.territoire in ["La Réunion", "Polynésie française"]:
                growth = 1 + 0.03 * i  # Croissance forte
            else:
                growth = 1 + 0.024 * i  # Croissance modérée
                
            noise = np.random.normal(1, 0.08)
            housing_benefits.append(base_housing * growth * noise)
        
        return housing_benefits
    
    def _simulate_solidarity_benefits(self, dates):
        """Simule les prestations de solidarité"""
        base_solidarity = self.config["budget_base"] * 0.20
        
        # Ajustement selon les spécificités
        multiplier = 1.5 if "precarite" in self.config["specificites"] else 1.0
        
        solidarity_benefits = []
        for i, date in enumerate(dates):
            if self.territoire in ["Mayotte", "Guyane"]:
                growth = 1 + 0.04 * i  # Croissance très forte
            elif self.territoire in ["La Réunion", "Polynésie française"]:
                growth = 1 + 0.035 * i  # Croissance forte
            else:
                growth = 1 + 0.028 * i  # Croissance modérée
                
            noise = np.random.normal(1, 0.09)
            solidarity_benefits.append(base_solidarity * growth * multiplier * noise)
        
        return solidarity_benefits
    
    def _simulate_management_costs(self, dates):
        """Simule les frais de gestion"""
        base_management = self.config["budget_base"] * 0.05
        
        management_costs = []
        for i, date in enumerate(dates):
            growth = 1 + 0.02 * i
            noise = np.random.normal(1, 0.04)
            management_costs.append(base_management * growth * noise)
        
        return management_costs
    
    def _simulate_coverage_rate(self, dates):
        """Simule le taux de couverture"""
        rates = []
        for i, date in enumerate(dates):
            if self.territoire in ["Mayotte", "Guyane"]:
                base_rate = 0.85  # Taux de couverture initial plus faible
            elif self.territoire in ["La Réunion", "Polynésie française"]:
                base_rate = 0.88  # Taux de couverture initial modéré
            else:
                base_rate = 0.92  # Taux de couverture initial élevé
            
            year = date.year
            if year >= 2010:
                improvement = 1 + 0.005 * (year - 2010)
            else:
                improvement = 1
            
            noise = np.random.normal(1, 0.03)
            rates.append(base_rate * improvement * noise)
        
        return rates
    
    def _simulate_management_ratio(self, dates):
        """Simule le ratio de gestion"""
        ratios = []
        for i, date in enumerate(dates):
            if self.territoire in ["Saint-Pierre-et-Miquelon", "Wallis-et-Futuna"]:
                base_ratio = 0.075  # Ratio de gestion initial plus élevé (petits territoires)
            elif self.territoire in ["Mayotte", "Guyane"]:
                base_ratio = 0.065  # Ratio de gestion initial modéré
            else:
                base_ratio = 0.055  # Ratio de gestion initial faible
            
            year = date.year
            if year >= 2010:
                improvement = 1 - 0.003 * (year - 2010)
            else:
                improvement = 1
            
            noise = np.random.normal(1, 0.02)
            ratios.append(base_ratio * improvement * noise)
        
        return ratios
    
    def _simulate_account_balance(self, dates):
        """Simule le solde de compte"""
        balances = []
        for i, date in enumerate(dates):
            base_balance = self.config["budget_base"] * 0.03
            
            year = date.year
            if year >= 2010:
                improvement = 1 + 0.01 * (year - 2010)
            else:
                improvement = 1
            
            noise = np.random.normal(1, 0.15)
            balances.append(base_balance * improvement * noise)
        
        return balances
    
    def _simulate_family_allocations(self, dates):
        """Simule les allocations familiales"""
        base_allocation = self.config["budget_base"] * 0.25
        
        # Ajustement selon les spécificités
        multiplier = 1.4 if "familles_nombreuses" in self.config["specificites"] else 1.0
        
        allocations = []
        for i, date in enumerate(dates):
            if self.territoire in ["Mayotte", "Guyane"]:
                growth = 1 + 0.03 * i  # Croissance très forte
            elif self.territoire in ["La Réunion", "Polynésie française"]:
                growth = 1 + 0.025 * i  # Croissance forte
            else:
                growth = 1 + 0.02 * i  # Croissance modérée
                
            noise = np.random.normal(1, 0.06)
            allocations.append(base_allocation * growth * multiplier * noise)
        
        return allocations
    
    def _simulate_ars(self, dates):
        """Simule l'Allocation de Rentrée Scolaire"""
        base_ars = self.config["budget_base"] * 0.08
        
        # Ajustement selon les spécificités
        multiplier = 1.3 if "jeunesse" in self.config["specificites"] else 1.0
        
        ars = []
        for i, date in enumerate(dates):
            if self.territoire in ["Mayotte", "Guyane"]:
                growth = 1 + 0.032 * i  # Croissance très forte
            elif self.territoire in ["La Réunion", "Polynésie française"]:
                growth = 1 + 0.028 * i  # Croissance forte
            else:
                growth = 1 + 0.022 * i  # Croissance modérée
                
            noise = np.random.normal(1, 0.07)
            ars.append(base_ars * growth * multiplier * noise)
        
        return ars
    
    def _simulate_apl(self, dates):
        """Simule les Aides Personnalisées au Logement"""
        base_apl = self.config["budget_base"] * 0.20
        
        apl = []
        for i, date in enumerate(dates):
            if self.territoire in ["Mayotte", "Guyane"]:
                growth = 1 + 0.036 * i  # Croissance très forte
            elif self.territoire in ["La Réunion", "Polynésie française"]:
                growth = 1 + 0.032 * i  # Croissance forte
            else:
                growth = 1 + 0.026 * i  # Croissance modérée
                
            noise = np.random.normal(1, 0.08)
            apl.append(base_apl * growth * noise)
        
        return apl
    
    def _simulate_rsa(self, dates):
        """Simule le Revenu de Solidarité Active"""
        base_rsa = self.config["budget_base"] * 0.15
        
        # Ajustement selon les spécificités
        multiplier = 1.6 if "precarite" in self.config["specificites"] else 1.0
        
        rsa = []
        for i, date in enumerate(dates):
            if self.territoire in ["Mayotte", "Guyane"]:
                growth = 1 + 0.042 * i  # Croissance très forte
            elif self.territoire in ["La Réunion", "Polynésie française"]:
                growth = 1 + 0.038 * i  # Croissance forte
            else:
                growth = 1 + 0.03 * i  # Croissance modérée
                
            noise = np.random.normal(1, 0.09)
            rsa.append(base_rsa * growth * multiplier * noise)
        
        return rsa
    
    def _simulate_birth_grant(self, dates):
        """Simule la prime à la naissance"""
        base_birth = self.config["budget_base"] * 0.04
        
        # Ajustement selon les spécificités
        multiplier = 1.5 if "jeunesse" in self.config["specificites"] else 1.0
        
        birth_grants = []
        for i, date in enumerate(dates):
            if self.territoire in ["Mayotte", "Guyane"]:
                growth = 1 + 0.026 * i  # Croissance très forte
            elif self.territoire in ["La Réunion", "Polynésie française"]:
                growth = 1 + 0.022 * i  # Croissance forte
            else:
                growth = 1 + 0.018 * i  # Croissance modérée
                
            noise = np.random.normal(1, 0.10)
            birth_grants.append(base_birth * growth * multiplier * noise)
        
        return birth_grants
    
    def _add_caf_trends(self, df):
        """Ajoute des tendances réalistes adaptées aux CAF DROM-COM"""
        for i, row in df.iterrows():
            year = row['Annee']
            
            # Développement initial (2002-2005)
            if 2002 <= year <= 2005:
                df.loc[i, 'Contributions_Etat'] *= 1.1
                df.loc[i, 'Prestations_Familiales'] *= 1.15
            
            # Réforme des prestations (2006-2010)
            if 2006 <= year <= 2010:
                df.loc[i, 'RSA'] *= 1.25  # Mise en place du RSA
                df.loc[i, 'Prestations_Solidarite'] *= 1.3
            
            # Impact de la crise financière (2008-2009)
            if 2008 <= year <= 2009:
                df.loc[i, 'Cotisations_Sociales'] *= 0.92
                df.loc[i, 'RSA'] *= 1.15
            
            # Renforcement des politiques sociales (2011-2015)
            elif 2011 <= year <= 2015:
                df.loc[i, 'Contributions_Etat'] *= 1.12
                df.loc[i, 'Allocations_Familiales'] *= 1.08
            
            # Mouvements sociaux de 2017 et renforcement des aides
            if year == 2017:
                df.loc[i, 'Contributions_Etat'] *= 1.18
                df.loc[i, 'RSA'] *= 1.10
            
            # Impact de la crise COVID-19 (2020-2021)
            if 2020 <= year <= 2021:
                if year == 2020:
                    df.loc[i, 'Cotisations_Sociales'] *= 0.85
                    df.loc[i, 'Contributions_Etat'] *= 1.25
                    df.loc[i, 'RSA'] *= 1.35
            
            # Plan de relance post-COVID (2022-2025)
            if year >= 2022:
                df.loc[i, 'Contributions_Etat'] *= 1.08
                df.loc[i, 'Prestations_Logement'] *= 1.12
                df.loc[i, 'ARS'] *= 1.10
    
    def create_financial_analysis(self, df):
        """Crée une analyse complète des finances de la CAF"""
        plt.style.use('seaborn-v0_8')
        fig = plt.figure(figsize=(20, 24))
        
        # 1. Évolution des recettes et dépenses
        ax1 = plt.subplot(4, 2, 1)
        self._plot_revenue_expenses(df, ax1)
        
        # 2. Structure des recettes
        ax2 = plt.subplot(4, 2, 2)
        self._plot_revenue_structure(df, ax2)
        
        # 3. Structure des dépenses
        ax3 = plt.subplot(4, 2, 3)
        self._plot_expenses_structure(df, ax3)
        
        # 4. Prestations versées
        ax4 = plt.subplot(4, 2, 4)
        self._plot_benefits(df, ax4)
        
        # 5. Indicateurs de performance
        ax5 = plt.subplot(4, 2, 5)
        self._plot_performance_indicators(df, ax5)
        
        # 6. Évolution des allocataires
        ax6 = plt.subplot(4, 2, 6)
        self._plot_allocataires(df, ax6)
        
        # 7. Détail des prestations familiales
        ax7 = plt.subplot(4, 2, 7)
        self._plot_family_benefits(df, ax7)
        
        # 8. Évolution du solde
        ax8 = plt.subplot(4, 2, 8)
        self._plot_balance(df, ax8)
        
        plt.suptitle(f'Analyse des Comptes de CAF {self.territoire} ({self.start_year}-{self.end_year})', 
                    fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'CAF_{self.territoire}_financial_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Générer les insights
        self._generate_financial_insights(df)
    
    def _plot_revenue_expenses(self, df, ax):
        """Plot de l'évolution des recettes et dépenses"""
        ax.plot(df['Annee'], df['Recettes_Totales'], label='Recettes Totales', 
               linewidth=2, color='#2A9D8F', alpha=0.8)
        ax.plot(df['Annee'], df['Depenses_Totales'], label='Dépenses Totales', 
               linewidth=2, color='#E76F51', alpha=0.8)
        
        ax.set_title('Évolution des Recettes et Dépenses (M€)', 
                    fontsize=12, fontweight='bold')
        ax.set_ylabel('Montants (M€)')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_revenue_structure(self, df, ax):
        """Plot de la structure des recettes"""
        years = df['Annee']
        width = 0.8
        
        bottom = np.zeros(len(years))
        categories = ['Cotisations_Sociales', 'Contributions_Etat', 'Autres_Recettes']
        colors = ['#264653', '#2A9D8F', '#E76F51']
        labels = ['Cotisations Sociales', 'Contributions État', 'Autres Recettes']
        
        for i, category in enumerate(categories):
            ax.bar(years, df[category], width, label=labels[i], bottom=bottom, color=colors[i])
            bottom += df[category]
        
        ax.set_title('Structure des Recettes (M€)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Montants (M€)')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
    
    def _plot_expenses_structure(self, df, ax):
        """Plot de la structure des dépenses"""
        years = df['Annee']
        width = 0.8
        
        bottom = np.zeros(len(years))
        categories = ['Prestations_Familiales', 'Prestations_Logement', 
                     'Prestations_Solidarite', 'Frais_Gestion']
        colors = ['#264653', '#2A9D8F', '#E76F51', '#F9A602']
        labels = ['Prestations Familiales', 'Prestations Logement', 
                 'Prestations Solidarité', 'Frais de Gestion']
        
        for i, category in enumerate(categories):
            ax.bar(years, df[category], width, label=labels[i], bottom=bottom, color=colors[i])
            bottom += df[category]
        
        ax.set_title('Structure des Dépenses (M€)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Montants (M€)')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
    
    def _plot_benefits(self, df, ax):
        """Plot des prestations versées"""
        ax.plot(df['Annee'], df['Allocations_Familiales'], label='Allocations Familiales', 
               linewidth=2, color='#264653', alpha=0.8)
        ax.plot(df['Annee'], df['ARS'], label='ARS', 
               linewidth=2, color='#2A9D8F', alpha=0.8)
        ax.plot(df['Annee'], df['APL'], label='APL', 
               linewidth=2, color='#E76F51', alpha=0.8)
        ax.plot(df['Annee'], df['RSA'], label='RSA', 
               linewidth=2, color='#F9A602', alpha=0.8)
        ax.plot(df['Annee'], df['Prime_Naissance'], label='Prime Naissance', 
               linewidth=2, color='#6A0572', alpha=0.8)
        
        ax.set_title('Détail des Prestations Versées (M€)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Montants (M€)')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_performance_indicators(self, df, ax):
        """Plot des indicateurs de performance"""
        # Taux de couverture
        ax.plot(df['Annee'], df['Taux_Couverture'], label='Taux de Couverture', 
               linewidth=2, color='#2A9D8F', alpha=0.8)
        
        ax.set_title('Indicateurs de Performance', fontsize=12, fontweight='bold')
        ax.set_ylabel('Taux de Couverture', color='#2A9D8F')
        ax.tick_params(axis='y', labelcolor='#2A9D8F')
        ax.grid(True, alpha=0.3)
        
        # Ratio de gestion en second axe
        ax2 = ax.twinx()
        ax2.plot(df['Annee'], df['Ratio_Gestion'], label='Ratio de Gestion', 
                linewidth=2, color='#E76F51', alpha=0.8)
        ax2.set_ylabel('Ratio de Gestion', color='#E76F51')
        ax2.tick_params(axis='y', labelcolor='#E76F51')
        
        # Combiner les légendes
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    def _plot_allocataires(self, df, ax):
        """Plot de l'évolution du nombre d'allocataires"""
        ax.plot(df['Annee'], df['Nombre_Allocataires'], label='Nombre d\'Allocataires', 
               linewidth=2, color='#264653', alpha=0.8)
        
        ax.set_title('Évolution du Nombre d\'Allocataires', fontsize=12, fontweight='bold')
        ax.set_ylabel('Nombre d\'Allocataires', color='#264653')
        ax.tick_params(axis='y', labelcolor='#264653')
        ax.grid(True, alpha=0.3)
        
        # Prestations versées en second axe
        ax2 = ax.twinx()
        ax2.plot(df['Annee'], df['Prestations_Versees'], label='Prestations Versées (M€)', 
                linewidth=2, color='#E76F51', alpha=0.8)
        ax2.set_ylabel('Prestations Versées (M€)', color='#E76F51')
        ax2.tick_params(axis='y', labelcolor='#E76F51')
        
        # Combiner les légendes
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    def _plot_family_benefits(self, df, ax):
        """Plot du détail des prestations familiales"""
        years = df['Annee']
        width = 0.8
        
        bottom = np.zeros(len(years))
        categories = ['Allocations_Familiales', 'ARS', 'Prime_Naissance']
        colors = ['#264653', '#2A9D8F', '#E76F51']
        labels = ['Allocations Familiales', 'ARS', 'Prime Naissance']
        
        for i, category in enumerate(categories):
            ax.bar(years, df[category], width, label=labels[i], bottom=bottom, color=colors[i])
            bottom += df[category]
        
        ax.set_title('Détail des Prestations Familiales (M€)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Montants (M€)')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
    
    def _plot_balance(self, df, ax):
        """Plot de l'évolution du solde"""
        ax.bar(df['Annee'], df['Solde_Compte'], label='Solde (M€)', 
              color='#2A9D8F', alpha=0.7)
        
        ax.set_title('Évolution du Solde de Compte', fontsize=12, fontweight='bold')
        ax.set_ylabel('Solde (M€)', color='#2A9D8F')
        ax.tick_params(axis='y', labelcolor='#2A9D8F')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Ligne de tendance
        z = np.polyfit(df['Annee'], df['Solde_Compte'], 1)
        p = np.poly1d(z)
        ax.plot(df['Annee'], p(df['Annee']), "r--", alpha=0.8)
    
    def _generate_financial_insights(self, df):
        """Génère des insights analytiques adaptés aux CAF DROM-COM"""
        print(f"🏛️ INSIGHTS ANALYTIQUES - CAF {self.territoire}")
        print("=" * 60)
        
        # 1. Statistiques de base
        print("\n1. 📈 STATISTIQUES GÉNÉRALES:")
        avg_revenue = df['Recettes_Totales'].mean()
        avg_expenses = df['Depenses_Totales'].mean()
        avg_balance = df['Solde_Compte'].mean()
        avg_allocataires = df['Nombre_Allocataires'].mean()
        
        print(f"Recettes moyennes annuelles: {avg_revenue:.2f} M€")
        print(f"Dépenses moyennes annuelles: {avg_expenses:.2f} M€")
        print(f"Solde moyen annuel: {avg_balance:.2f} M€")
        print(f"Nombre moyen d'allocataires: {avg_allocataires:.0f}")
        
        # 2. Croissance
        print("\n2. 📊 TAUX DE CROISSANCE:")
        revenue_growth = ((df['Recettes_Totales'].iloc[-1] / 
                          df['Recettes_Totales'].iloc[0]) - 1) * 100
        allocataires_growth = ((df['Nombre_Allocataires'].iloc[-1] / 
                               df['Nombre_Allocataires'].iloc[0]) - 1) * 100
        
        print(f"Croissance des recettes ({self.start_year}-{self.end_year}): {revenue_growth:.1f}%")
        print(f"Croissance du nombre d'allocataires ({self.start_year}-{self.end_year}): {allocataires_growth:.1f}%")
        
        # 3. Structure financière
        print("\n3. 📋 STRUCTURE FINANCIÈRE:")
        cotisations_share = (df['Cotisations_Sociales'].mean() / df['Recettes_Totales'].mean()) * 100
        etat_share = (df['Contributions_Etat'].mean() / df['Recettes_Totales'].mean()) * 100
        prestations_share = (df['Prestations_Versees'].mean() / df['Depenses_Totales'].mean()) * 100
        
        print(f"Part des cotisations sociales dans les recettes: {cotisations_share:.1f}%")
        print(f"Part des contributions de l'État dans les recettes: {etat_share:.1f}%")
        print(f"Part des prestations dans les dépenses: {prestations_share:.1f}%")
        
        # 4. Performance
        print("\n4. 🎯 PERFORMANCE:")
        avg_coverage = df['Taux_Couverture'].mean() * 100
        avg_management_ratio = df['Ratio_Gestion'].mean() * 100
        last_balance = df['Solde_Compte'].iloc[-1]
        
        print(f"Taux de couverture moyen: {avg_coverage:.1f}%")
        print(f"Ratio de gestion moyen: {avg_management_ratio:.1f}%")
        print(f"Solde final: {last_balance:.2f} M€")
        
        # 5. Spécificités du territoire
        print(f"\n5. 🌟 SPÉCIFICITÉS DE {self.territoire.upper()}:")
        print(f"Spécialités: {', '.join(self.config['specificites'])}")
        
        # 6. Événements marquants
        print("\n6. 📅 ÉVÉNEMENTS MARQUANTS:")
        print("• 2002-2005: Développement initial des services CAF")
        print("• 2006-2010: Réforme des prestations et mise en place du RSA")
        print("• 2008-2009: Impact de la crise financière sur les cotisations")
        print("• 2011-2015: Renforcement des politiques sociales")
        print("• 2017: Mouvements sociaux et renforcement des aides")
        print("• 2020-2021: Crise COVID-19 et plans de soutien exceptionnels")
        print("• 2022-2025: Plan de relance post-COVID")
        
        # 7. Recommandations
        print("\n7. 💡 RECOMMANDATIONS STRATÉGIQUES:")
        if "precarite" in self.config["specificites"]:
            print("• Renforcer les dispositifs de lutte contre la précarité")
            print("• Développer les accompagnements vers l'emploi")
        if "familles_nombreuses" in self.config["specificites"]:
            print("• Adapter les prestations aux spécificités des familles nombreuses")
            print("• Développer les services de soutien à la parentalité")
        if "jeunesse" in self.config["specificites"]:
            print("• Renforcer les aides à l'éducation et la formation")
            print("• Développer les programmes d'insertion professionnelle des jeunes")
        if "isolement" in self.config["specificites"]:
            print("• Développer les services à distance et la dématérialisation")
            print("• Renforcer les partenariats locaux pour améliorer l'accès aux droits")
        print("• Améliorer la digitalisation des services")
        print("• Renforcer la prévention des impayés et le recouvrement")
        print("• Optimiser la gestion des fonds pour maintenir l'équilibre financier")

def main():
    """Fonction principale pour les CAF DROM-COM"""
    # Liste des 10 DROM-COM
    territoires = [
        "Guadeloupe", "Martinique", "Guyane", "La Réunion", "Mayotte",
        "Saint-Martin", "Saint-Barthélemy", "Saint-Pierre-et-Miquelon",
        "Wallis-et-Futuna", "Polynésie française", "Nouvelle-Calédonie"
    ]
    
    print("🏛️ ANALYSE DES COMPTES DES CAF DES 10 DROM-COM (2002-2025)")
    print("=" * 60)
    
    # Demander à l'utilisateur de choisir un territoire
    print("Liste des territoires disponibles:")
    for i, territoire in enumerate(territoires, 1):
        print(f"{i}. {territoire}")
    
    try:
        choix = int(input("\nChoisissez le numéro du territoire à analyser: "))
        if choix < 1 or choix > len(territoires):
            raise ValueError
        territoire_selectionne = territoires[choix-1]
    except (ValueError, IndexError):
        print("Choix invalide. Sélection de La Réunion par défaut.")
        territoire_selectionne = "La Réunion"
    
    # Initialiser l'analyseur
    analyzer = CAF_DROMCOMAnalyzer(territoire_selectionne)
    
    # Générer les données
    financial_data = analyzer.generate_financial_data()
    
    # Sauvegarder les données
    output_file = f'CAF_{territoire_selectionne}_financial_data_2002_2025.csv'
    financial_data.to_csv(output_file, index=False)
    print(f"💾 Données sauvegardées: {output_file}")
    
    # Aperçu des données
    print("\n👀 Aperçu des données:")
    print(financial_data[['Annee', 'Nombre_Allocataires', 'Recettes_Totales', 'Depenses_Totales', 'Solde_Compte']].head())
    
    # Créer l'analyse
    print("\n📈 Création de l'analyse financière...")
    analyzer.create_financial_analysis(financial_data)
    
    print(f"\n✅ Analyse des comptes de CAF {territoire_selectionne} terminée!")
    print(f"📊 Période: {analyzer.start_year}-{analyzer.end_year}")
    print("📦 Données: Allocataires, prestations, recettes, dépenses, solde")

if __name__ == "__main__":
    main()