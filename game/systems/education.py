"""
Educational Content System - Manages cloud concepts, learning modules, and quizzes
"""

import pygame
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class ConceptCategory(Enum):
    """Categories of cloud concepts"""
    COMPUTE = "compute"
    STORAGE = "storage"
    NETWORKING = "networking"
    SECURITY = "security"
    DEVOPS = "devops"

@dataclass
class CloudConcept:
    """Represents a cloud computing concept to be learned"""
    id: str
    name: str
    category: ConceptCategory
    description: str
    detailed_content: str
    prerequisites: List[str]  # IDs of required concepts
    unlock_ability: Optional[str] = None
    difficulty_level: int = 1  # 1-5 scale

@dataclass
class QuizQuestion:
    """Represents a quiz question"""
    question: str
    options: List[str]
    correct_answer: int  # Index of correct option
    explanation: str
    concept_id: str

class LearningModule:
    """Interactive learning module for a specific cloud concept"""
    
    def __init__(self, concept: CloudConcept, questions: List[QuizQuestion]):
        self.concept = concept
        self.questions = questions
        self.current_question = 0
        self.score = 0
        self.completed = False
        self.attempts = 0
        self.max_attempts = 3
    
    def get_current_question(self) -> Optional[QuizQuestion]:
        """Get the current quiz question"""
        if self.current_question < len(self.questions):
            return self.questions[self.current_question]
        return None
    
    def answer_question(self, answer_index: int) -> Tuple[bool, str]:
        """Answer the current question and return (correct, explanation)"""
        question = self.get_current_question()
        if not question:
            return False, "No question available"
        
        is_correct = answer_index == question.correct_answer
        
        if is_correct:
            self.score += 1
            self.current_question += 1
        else:
            self.attempts += 1
        
        # Check if module is completed
        if self.current_question >= len(self.questions):
            self.completed = True
        elif self.attempts >= self.max_attempts:
            self.completed = True  # Failed completion
        
        return is_correct, question.explanation
    
    def get_progress(self) -> Tuple[int, int]:
        """Get current progress (current, total)"""
        return (self.current_question, len(self.questions))
    
    def get_score_percentage(self) -> float:
        """Get score as percentage"""
        if len(self.questions) == 0:
            return 0.0
        return (self.score / len(self.questions)) * 100
    
    def is_passed(self) -> bool:
        """Check if module was passed (70% or higher)"""
        return self.completed and self.get_score_percentage() >= 70.0

class EducationSystem:
    """Manages all educational content and player learning progress"""
    
    def __init__(self):
        self.concepts: Dict[str, CloudConcept] = {}
        self.quiz_questions: Dict[str, List[QuizQuestion]] = {}
        self.player_progress: Dict[str, bool] = {}  # concept_id -> completed
        self.unlocked_abilities: List[str] = []
        
        # Initialize content
        self._initialize_concepts()
        self._initialize_quiz_questions()
    
    def _initialize_concepts(self):
        """Initialize cloud computing concepts"""
        # Compute concepts
        self.concepts["ec2_basics"] = CloudConcept(
            id="ec2_basics",
            name="EC2 Basics",
            category=ConceptCategory.COMPUTE,
            description="Learn about Amazon EC2 virtual servers",
            detailed_content="""
Amazon Elastic Compute Cloud (EC2) provides scalable virtual servers in the cloud.

Key Features:
• Virtual machines called instances
• Multiple instance types for different workloads
• Pay-as-you-go pricing model
• Global availability across regions
• Auto Scaling capabilities

Instance Types:
• General Purpose (t3, m5): Balanced CPU, memory, networking
• Compute Optimized (c5): High-performance processors
• Memory Optimized (r5): Fast performance for memory-intensive workloads
• Storage Optimized (i3): High sequential read/write access

Best Practices:
• Choose the right instance type for your workload
• Use Auto Scaling for variable demand
• Implement proper security groups
• Regular backups with snapshots
            """,
            prerequisites=[],
            unlock_ability="auto_scaling",
            difficulty_level=1
        )
        
        self.concepts["lambda_serverless"] = CloudConcept(
            id="lambda_serverless",
            name="AWS Lambda & Serverless",
            category=ConceptCategory.COMPUTE,
            description="Serverless computing with AWS Lambda",
            detailed_content="""
AWS Lambda lets you run code without provisioning servers.

Key Benefits:
• No server management required
• Automatic scaling
• Pay only for compute time used
• Built-in fault tolerance
• Integrates with many AWS services

Use Cases:
• Event-driven processing
• Real-time file processing
• Web application backends
• IoT data processing
• Scheduled tasks

Best Practices:
• Keep functions small and focused
• Optimize cold start times
• Use environment variables for configuration
• Implement proper error handling
• Monitor with CloudWatch
            """,
            prerequisites=["ec2_basics"],
            unlock_ability="serverless_deploy",
            difficulty_level=2
        )
        
        # Storage concepts
        self.concepts["s3_storage"] = CloudConcept(
            id="s3_storage",
            name="Amazon S3 Storage",
            category=ConceptCategory.STORAGE,
            description="Object storage with Amazon S3",
            detailed_content="""
Amazon Simple Storage Service (S3) provides object storage in the cloud.

Key Features:
• Virtually unlimited storage capacity
• 99.999999999% (11 9's) durability
• Multiple storage classes for cost optimization
• Global accessibility via web interface
• Versioning and lifecycle management

Storage Classes:
• Standard: Frequently accessed data
• Intelligent-Tiering: Automatic cost optimization
• Glacier: Long-term archival
• Deep Archive: Lowest cost archival

Security Features:
• Encryption at rest and in transit
• Access control with IAM policies
• Bucket policies and ACLs
• VPC endpoints for private access
            """,
            prerequisites=[],
            unlock_ability="data_backup",
            difficulty_level=1
        )
        
        # Networking concepts
        self.concepts["vpc_networking"] = CloudConcept(
            id="vpc_networking",
            name="VPC Networking",
            category=ConceptCategory.NETWORKING,
            description="Virtual Private Cloud networking",
            detailed_content="""
Amazon Virtual Private Cloud (VPC) provides isolated network environments.

Core Components:
• Subnets: Divide VPC into smaller networks
• Route Tables: Control traffic routing
• Internet Gateway: Connect to internet
• NAT Gateway: Outbound internet for private subnets
• Security Groups: Instance-level firewalls

Network Design:
• Public subnets for web servers
• Private subnets for databases
• Multiple Availability Zones for high availability
• CIDR block planning for IP addressing

Best Practices:
• Use multiple AZs for redundancy
• Implement defense in depth
• Monitor network traffic
• Use VPC Flow Logs for troubleshooting
            """,
            prerequisites=[],
            unlock_ability="network_isolation",
            difficulty_level=2
        )
        
        # Security concepts
        self.concepts["iam_security"] = CloudConcept(
            id="iam_security",
            name="IAM Security",
            category=ConceptCategory.SECURITY,
            description="Identity and Access Management",
            detailed_content="""
AWS Identity and Access Management (IAM) controls access to AWS resources.

Key Components:
• Users: Individual identities
• Groups: Collections of users
• Roles: Temporary access for services
• Policies: Define permissions

Security Principles:
• Principle of least privilege
• Use roles instead of users for applications
• Enable MFA for sensitive operations
• Regular access reviews and rotation

Best Practices:
• Never share access keys
• Use temporary credentials when possible
• Implement strong password policies
• Monitor access with CloudTrail
• Use policy conditions for fine-grained control
            """,
            prerequisites=[],
            unlock_ability="access_control",
            difficulty_level=2
        )
    
    def _initialize_quiz_questions(self):
        """Initialize quiz questions for each concept"""
        # EC2 Basics questions
        self.quiz_questions["ec2_basics"] = [
            QuizQuestion(
                question="What does EC2 stand for?",
                options=[
                    "Elastic Compute Cloud",
                    "Enhanced Cloud Computing",
                    "Enterprise Cloud Container",
                    "Elastic Container Cloud"
                ],
                correct_answer=0,
                explanation="EC2 stands for Elastic Compute Cloud, providing scalable virtual servers.",
                concept_id="ec2_basics"
            ),
            QuizQuestion(
                question="Which EC2 instance type is best for memory-intensive applications?",
                options=[
                    "t3 (General Purpose)",
                    "c5 (Compute Optimized)",
                    "r5 (Memory Optimized)",
                    "i3 (Storage Optimized)"
                ],
                correct_answer=2,
                explanation="R5 instances are memory optimized, designed for memory-intensive workloads.",
                concept_id="ec2_basics"
            ),
            QuizQuestion(
                question="What is the main benefit of EC2 Auto Scaling?",
                options=[
                    "Reduces costs by shutting down unused instances",
                    "Automatically adjusts capacity based on demand",
                    "Provides better security for instances",
                    "Increases network performance"
                ],
                correct_answer=1,
                explanation="Auto Scaling automatically adjusts the number of instances based on demand, ensuring optimal performance and cost.",
                concept_id="ec2_basics"
            )
        ]
        
        # Lambda questions
        self.quiz_questions["lambda_serverless"] = [
            QuizQuestion(
                question="What is the main advantage of serverless computing?",
                options=[
                    "Better performance than traditional servers",
                    "No server management required",
                    "Lower latency for all applications",
                    "Unlimited execution time"
                ],
                correct_answer=1,
                explanation="Serverless computing eliminates the need to manage servers, allowing developers to focus on code.",
                concept_id="lambda_serverless"
            ),
            QuizQuestion(
                question="How does AWS Lambda pricing work?",
                options=[
                    "Fixed monthly fee per function",
                    "Pay per server hour used",
                    "Pay only for compute time consumed",
                    "Free for all usage"
                ],
                correct_answer=2,
                explanation="Lambda uses pay-per-use pricing - you only pay for the compute time your code actually consumes.",
                concept_id="lambda_serverless"
            )
        ]
        
        # S3 questions
        self.quiz_questions["s3_storage"] = [
            QuizQuestion(
                question="What is Amazon S3's durability rating?",
                options=[
                    "99.9% (three 9's)",
                    "99.99% (four 9's)",
                    "99.999999999% (eleven 9's)",
                    "100% guaranteed"
                ],
                correct_answer=2,
                explanation="S3 provides 99.999999999% (11 9's) durability, meaning extremely low probability of data loss.",
                concept_id="s3_storage"
            ),
            QuizQuestion(
                question="Which S3 storage class is most cost-effective for long-term archival?",
                options=[
                    "S3 Standard",
                    "S3 Intelligent-Tiering",
                    "S3 Glacier",
                    "S3 Glacier Deep Archive"
                ],
                correct_answer=3,
                explanation="S3 Glacier Deep Archive offers the lowest cost for long-term archival with retrieval times of 12+ hours.",
                concept_id="s3_storage"
            )
        ]
        
        # VPC questions
        self.quiz_questions["vpc_networking"] = [
            QuizQuestion(
                question="What is the purpose of a NAT Gateway in a VPC?",
                options=[
                    "Provide internet access to public subnets",
                    "Allow private subnets to access the internet",
                    "Connect multiple VPCs together",
                    "Provide DNS resolution"
                ],
                correct_answer=1,
                explanation="NAT Gateway allows instances in private subnets to access the internet while remaining private.",
                concept_id="vpc_networking"
            ),
            QuizQuestion(
                question="What is the recommended practice for high availability in VPC design?",
                options=[
                    "Use only one large subnet",
                    "Deploy across multiple Availability Zones",
                    "Use only private subnets",
                    "Avoid using security groups"
                ],
                correct_answer=1,
                explanation="Deploying across multiple Availability Zones provides redundancy and high availability.",
                concept_id="vpc_networking"
            )
        ]
        
        # IAM questions
        self.quiz_questions["iam_security"] = [
            QuizQuestion(
                question="What is the principle of least privilege in IAM?",
                options=[
                    "Give users maximum permissions for convenience",
                    "Grant only the minimum permissions needed",
                    "Use only root account access",
                    "Avoid using policies altogether"
                ],
                correct_answer=1,
                explanation="Principle of least privilege means granting only the minimum permissions necessary to perform required tasks.",
                concept_id="iam_security"
            ),
            QuizQuestion(
                question="When should you use IAM roles instead of users?",
                options=[
                    "For human administrators only",
                    "For applications and AWS services",
                    "Never, users are always better",
                    "Only for temporary access"
                ],
                correct_answer=1,
                explanation="IAM roles are preferred for applications and AWS services as they provide temporary, rotating credentials.",
                concept_id="iam_security"
            )
        ]
    
    def get_concept(self, concept_id: str) -> Optional[CloudConcept]:
        """Get a concept by ID"""
        return self.concepts.get(concept_id)
    
    def get_available_concepts(self, learned_concepts: List[str]) -> List[CloudConcept]:
        """Get concepts that can be learned based on prerequisites"""
        available = []
        for concept in self.concepts.values():
            if concept.id not in learned_concepts:
                # Check if prerequisites are met
                prerequisites_met = all(
                    prereq in learned_concepts 
                    for prereq in concept.prerequisites
                )
                if prerequisites_met:
                    available.append(concept)
        return available
    
    def create_learning_module(self, concept_id: str) -> Optional[LearningModule]:
        """Create a learning module for a concept"""
        concept = self.get_concept(concept_id)
        questions = self.quiz_questions.get(concept_id, [])
        
        if concept and questions:
            return LearningModule(concept, questions)
        return None
    
    def complete_concept(self, concept_id: str, player) -> bool:
        """Mark a concept as completed and unlock abilities"""
        if concept_id in self.concepts:
            self.player_progress[concept_id] = True
            
            # Add to player's learned concepts
            if hasattr(player, 'learn_concept'):
                player.learn_concept(concept_id)
            
            # Unlock ability if available
            concept = self.concepts[concept_id]
            if concept.unlock_ability and concept.unlock_ability not in self.unlocked_abilities:
                self.unlocked_abilities.append(concept.unlock_ability)
                if hasattr(player, 'current_abilities'):
                    player.current_abilities.append(concept.unlock_ability)
                print(f"Unlocked new ability: {concept.unlock_ability}")
            
            return True
        return False
    
    def get_learning_progress(self) -> Dict[str, float]:
        """Get learning progress by category"""
        progress = {}
        for category in ConceptCategory:
            category_concepts = [c for c in self.concepts.values() if c.category == category]
            if category_concepts:
                completed = sum(1 for c in category_concepts if self.player_progress.get(c.id, False))
                progress[category.value] = (completed / len(category_concepts)) * 100
            else:
                progress[category.value] = 0.0
        return progress