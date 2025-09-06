'use client'
import React, { useState } from 'react';
import { ArrowLeft, Check, CreditCard } from 'lucide-react';
import { Button, ProgressBar, ChatBubble, Chip } from '@/components/ui';
import { useApp } from '@/lib/context';
import { mockPendingActions } from '@/lib/mockData';
import { formatCurrency } from '@/lib/utils';

export const ApprovalsScreen: React.FC = () => {
  const { state, setCurrentScreen, setApprovals } = useApp();
  const { approvals } = state;
  const [activeTab, setActiveTab] = useState<'pending' | 'executed'>('pending');

  const handleApprove = (actionId: number) => {
    setApprovals({ ...approvals, [actionId]: true });
    
    // Check if quorum is reached
    const action = mockPendingActions.find(a => a.id === actionId);
    if (action && action.approvals + 1 >= action.required) {
      setTimeout(() => {
        alert('Action approved and executed! 🎉');
      }, 500);
    } else {
      setTimeout(() => {
        alert('You approved. More approvals needed.');
      }, 500);
    }
  };

  const pendingActions = mockPendingActions.filter(action => 
    action.approvals < action.required
  );

  const executedActions = mockPendingActions.filter(action => 
    action.approvals >= action.required
  );

  return (
    <div className="min-h-screen bg-white p-6">
      {/* Header */}
      <div className="flex items-center mb-6">
        <button onClick={() => setCurrentScreen('trip-detail')}>
          <ArrowLeft className="w-6 h-6" />
        </button>
        <h1 className="text-xl font-bold ml-4">Approvals</h1>
      </div>

      {/* Tabs */}
      <div className="flex mb-6">
        <button 
          onClick={() => setActiveTab('pending')}
          className={`flex-1 pb-2 border-b-2 font-medium transition-colors ${
            activeTab === 'pending' 
              ? 'border-blue-500 text-blue-600' 
              : 'border-transparent text-gray-500'
          }`}
        >
          Pending ({pendingActions.length})
        </button>
        <button 
          onClick={() => setActiveTab('executed')}
          className={`flex-1 pb-2 border-b-2 font-medium transition-colors ${
            activeTab === 'executed' 
              ? 'border-blue-500 text-blue-600' 
              : 'border-transparent text-gray-500'
          }`}
        >
          Executed ({executedActions.length})
        </button>
      </div>

      {/* Info Message */}
      <div className="mb-4">
        <ChatBubble message="75% member approval required for all actions." sender="left" />
      </div>

      {/* Actions List */}
      <div className="space-y-4">
        {(activeTab === 'pending' ? pendingActions : executedActions).map(action => {
          const isApproved = approvals[action.id];
          const progressPercentage = Math.round((action.approvals / action.required) * 100);
          const isQuorumReached = action.approvals >= action.required;

          return (
            <div key={action.id} className="p-4 border border-gray-200 rounded-xl">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <h3 className="font-medium">{action.type}: {formatCurrency(action.amount)} USDC</h3>
                  <p className="text-sm text-gray-600">{action.description}</p>
                </div>
                <CreditCard className="w-5 h-5 text-gray-400" />
              </div>
              
              <div className="mb-3">
                <div className="flex justify-between text-sm text-gray-600 mb-1">
                  <span>{action.approvals}/{action.required} approvals</span>
                  <span>{progressPercentage}%</span>
                </div>
                <ProgressBar current={action.approvals} total={action.required} />
              </div>
              
              <div className="flex items-center justify-between">
                <div className="flex -space-x-2">
                  {action.members.map((member, idx) => (
                    <div 
                      key={idx} 
                      className={`w-8 h-8 rounded-full border-2 border-white flex items-center justify-center text-xs font-medium ${
                        idx < action.approvals 
                          ? 'bg-green-500 text-white' 
                          : 'bg-gray-300 text-gray-600'
                      }`}
                    >
                      {idx < action.approvals ? (
                        <Check className="w-4 h-4" />
                      ) : (
                        member[0].toUpperCase()
                      )}
                    </div>
                  ))}
                </div>
                
                {activeTab === 'pending' && (
                  <Button 
                    variant={isApproved ? "secondary" : "primary"}
                    onClick={() => handleApprove(action.id)}
                    disabled={isApproved || isQuorumReached}
                    size="sm"
                  >
                    {isApproved ? 'Approved' : 'Approve'}
                  </Button>
                )}
                
                {activeTab === 'executed' && (
                  <Chip variant="success">Executed</Chip>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Empty State */}
      {activeTab === 'pending' && pendingActions.length === 0 && (
        <div className="text-center py-12">
          <ChatBubble message="No pending actions! 🎉" sender="left" />
        </div>
      )}

      {activeTab === 'executed' && executedActions.length === 0 && (
        <div className="text-center py-12">
          <ChatBubble message="No executed actions yet." sender="left" />
        </div>
      )}
    </div>
  );
};
