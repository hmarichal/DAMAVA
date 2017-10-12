#ifndef TIMER_H
#define TIMER_H

#define CUENTA 10
class Timer{
	public:
		Timer();
		void SetFlag(int* flag_timeout_main);
		void Init(void);
	private:
		static int *_flagTimer;
		
};

#endif
